import os
import re
import logging
import warnings
from typing import Union, Optional, Tuple
import concurrent.futures
import pandas as pd
import numpy as np
import tabula
from PyPDF2 import PdfReader
from psycopg2 import OperationalError, extensions
from tqdm import tqdm
from ktdparser.config import settings
from ktdparser.db import get_db


warnings.simplefilter(action="ignore", category=FutureWarning)


def log_msg(logger: Union[logging.Logger, None], level: int, log_message: str, *args) -> None:
    """Log a message if a logger is provided"""
    if logger:
        logger.log(level, log_message, *args)


class KTDParserError(Exception):
    """KTDParser error"""


class KTDParser:
    """KTDParser"""
    FORM_AREA_TOP = (25, 15)
    FORM_COLUMNS_AREA_SUBTASK = [56.07, 722.54, 780.11]
    FORM_COLUMNS_AREA_SUMMARY_TASK = [56.07, 94.2, 130.82, 329.66, 522.58, 626.26, 659.23]
    FORM_COLUMNS_AREA_OBJECT = [56.07, 94.2]
    PATTERNS = {
        "headers": [
            re.compile(r"^\s*Цех\s*Номер"),
            re.compile(r"^\s*Наименование\s*детали"),
            re.compile(r"^\s*Наименование,\s*марка"),
            re.compile(r"^\s*НПП\s*Обозначение,\s*наименование")
        ],
        "form_title1": re.compile(r"^\s*(?:Форма\s*)?(ТЛ|TЛ)\s*-\s*1"),
        "form_title2": re.compile(r"^\s*(?:Форма\s*)?(ТЛ|TЛ)\s*-\s*2"),
        "form_name1": re.compile(r"^\s*(?:Форма\s*)?(ВОК|МК|MK|BOK|КТП)\s*-\s*1"),
        "form_name2": re.compile(r"^\s*(?:Форма\s*)?(ВОК|МК|MK|BOK|КТП)\s*-\s*2"),
        "prof": re.compile(r"([^0-9]*)(\d+)$")
    }

    def __init__(self) -> None:
        """Initialize KTDParser"""
        self.file_path = None
        self.sections = []
        self.page_count = None
        self.ktd_page = None
        self.ktd_id = None
        self.tables = {}
        self.form_area_top = None
        self.columns_area_subtask = None
        self.columns_area_summary_task = None
        self.columns_area_object = None
        self.connection = None
        self.logger = None
        self.tqdm_disable = True
        self.page_offset = 0

    def parse_pdf(self, file_path: str, progressbar: bool = False, log: Union[bool, str] = False,
                  form_top: Optional[Tuple[Union[int, float], ...]] = None,
                  columns: Optional[Tuple[Union[int, float], ...]] = None,
                  workers: Optional[int] = None) -> None:
        """Parse a PDF file to extract KTD data.

        Args:
            file_path: The path to the PDF file to be parsed.
                       It should be a valid file path pointing to the PDF file.
                       The file must exist, and its extension must be '.pdf'.
            progressbar: Show progress bar.
            log: Write to log. If True, log to default location. If False, do not log.
                 If str, specify the path to the log file.
            form_top: The relative distance (%) from the top of the page to the table,
                      excluding the table headers on the first page of the form, and the rest.
                      If not specified, form_top will be (25, 15).
            columns: X-Coordinates of the columns (9).
                     If not specified, columns will be
                     (56.07, 94.2, 130.82, 329.66, 522.58, 626.26, 659.23, 722.54, 780.11).
            workers: The number of workers to use for parallel parsing

        Example:
            parse_pdf("ktd.pdf", progressbar=True, log="ktd.log")

        Raises:
            FileNotFoundError: If the file is not found, or if it is not a PDF.
            ValueError: If the parameters are invalid.
        """
        log_msg(self.logger, logging.INFO, "Extracting data from %s", file_path)
        self.file_path = file_path
        if not os.path.exists(self.file_path):
            log_msg(self.logger, logging.CRITICAL, "File %s not found", file_path)
            raise FileNotFoundError("File not found")
        if os.path.splitext(self.file_path)[1].lower() != ".pdf":
            log_msg(self.logger, logging.CRITICAL, "File %s is not a PDF", file_path)
            raise FileNotFoundError("File is not a PDF")
        if form_top:
            if len(form_top) == 2 and all(isinstance(x, (int, float)) for x in form_top):
                self.form_area_top = form_top
            else:
                raise ValueError("Invalid form_top param")
        else:
            self.form_area_top = self.FORM_AREA_TOP
        if columns:
            if len(columns) == 9 and all(isinstance(x, (int, float)) for x in columns):
                self.columns_area_subtask = [columns[0], columns[-2], columns[-1]]
                self.columns_area_summary_task = columns[:-2]
                self.columns_area_object = [columns[0], columns[1]]
            else:
                raise ValueError("Invalid columns param")
        else:
            self.columns_area_subtask = self.FORM_COLUMNS_AREA_SUBTASK
            self.columns_area_summary_task = self.FORM_COLUMNS_AREA_SUMMARY_TASK
            self.columns_area_object = self.FORM_COLUMNS_AREA_OBJECT
        if log:
            self.logger = logging.getLogger(__name__)
            logging.basicConfig(
                filename=settings.log_path if isinstance(log, bool) else log,
                level=logging.INFO,
                format="%(asctime)s.%(msecs)03d %(levelname)s: %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
                filemode="w"
            )
        if progressbar:
            self.tqdm_disable = False
        self._parse_file_structure()
        self._create_dataframes()
        ktd_id = self._parse_ktd_page()
        self.ktd_id = ktd_id
        if workers:
            self._parse_sections_parallel(ktd_id, workers)
        else:
            self._parse_sections(ktd_id)
        log_msg(self.logger, logging.INFO, "Data from file %s has been successfully extracted", file_path)

    def connect_to_db(self, password: str, user: Optional[str] = None, host: Optional[str] = None,
                      port: Optional[int] = None, database: Optional[str] = None) -> None:
        """Establish a connection to database and create KTD tables if not exist.

        Args:
            password: The password for the database user.
            user: The username for the database.
            host: The host address of the database.
            port: The port number of the database.
            database: The name of the database.
        """
        try:
            self.connection = get_db(password, user, host, port, database)
        except OperationalError as e:
            print(f"Connection or table creation error: {e}")

    def save_to_db(self) -> None:
        """Save KTD data in the database.

        Raises:
            KTDParserError: If No connection to the database or no parsed data
        """
        if not self.connection:
            raise KTDParserError("No connection to the database")
        if not self.tables:
            raise KTDParserError("No parsed data")
        extensions.register_adapter(np.int64, extensions.AsIs)
        extensions.register_adapter(np.float64, extensions.AsIs)
        for table in self.tables:
            if table == "ktd":
                self.tables[table] = self.tables[table].replace(float("nan"), None)
                continue
            self.tables[table] = self.tables[table].sort_values(by="page").replace(float("nan"), None)
        self.tables["material"]["quantity"] = self.tables["material"]["quantity"].str.replace(",", ".")
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM ktd WHERE id IN (%s)", (",".join(map(str, self.tables["ktd"]["id"])),))
        for i in range(len(self.tables["ktd"])):
            row = self.tables["ktd"].iloc[i].copy()
            cursor.execute("INSERT INTO ktd (id, name, page_count) VALUES (%(id)s, %(name)s, %(page_count)s)", row)
        self.tables["main_task"] = self.tables["main_task"].replace(float("nan"), None)
        main_task_ids = {}
        for i in range(len(self.tables["main_task"])):
            row = self.tables["main_task"].iloc[i].copy()
            cursor.execute("INSERT INTO main_task (ktd_id, name, page) VALUES (%(ktd_id)s, %(name)s, %(page)s) "
                           "RETURNING id", row)
            main_task_ids[row["id"]] = cursor.fetchone()[0]
        summary_task_ids = {}
        cursor.execute("SELECT MAX(id) FROM summary_task")
        last_summary_task_id = 1
        row = cursor.fetchone()
        if row and row[0]:
            last_summary_task_id = row[0]
        for i in range(len(self.tables["summary_task"])):
            row = self.tables["summary_task"].iloc[i].copy()
            if row["id"] not in summary_task_ids:
                if not summary_task_ids:
                    summary_task_ids[row["id"]] = last_summary_task_id
                else:
                    last_summary_task_id += 1
                    summary_task_ids[row["id"]] = last_summary_task_id
            row["main_task_id"] = main_task_ids[row["main_task_id"]]
            row["id"] = summary_task_ids[row["id"]]
            cursor.execute("INSERT INTO summary_task (main_task_id, id, code, object, name, docs, profession, "
                           "category, quantity, page) VALUES (%(main_task_id)s, %(id)s, %(code)s, %(object)s, "
                           "%(name)s, %(docs)s, %(profession)s, %(category)s, %(quantity)s, %(page)s)", row)
        for i in range(len(self.tables["object"])):
            row = self.tables["object"].iloc[i].copy()
            row["main_task_id"] = main_task_ids[row["main_task_id"]]
            cursor.execute("INSERT INTO object (ktd_id, main_task_id, code, name, page) VALUES (%(ktd_id)s, "
                           "%(main_task_id)s, %(code)s, %(name)s, %(page)s)", row)
        self.connection.commit()
        subtask_ids = {}
        for i in range(len(self.tables["subtask"])):
            row = self.tables["subtask"].iloc[i].copy()
            row["main_task_id"] = main_task_ids[row["main_task_id"]]
            row["summary_task_id"] = summary_task_ids[row["summary_task_id"]]
            cursor.execute("INSERT INTO subtask (ktd_id, main_task_id, summary_task_id, name, page) VALUES ("
                           "%(ktd_id)s, %(main_task_id)s, %(summary_task_id)s, %(name)s, %(page)s) RETURNING id", row)
            subtask_ids[row["id"]] = cursor.fetchone()[0]
        for i in range(len(self.tables["material"])):
            row = self.tables["material"].iloc[i].copy()
            row["main_task_id"] = main_task_ids[row["main_task_id"]]
            row["summary_task_id"] = summary_task_ids[row["summary_task_id"]]
            row["subtask_id"] = subtask_ids.get(row["subtask_id"], None)
            cursor.execute("INSERT INTO material (ktd_id, main_task_id, summary_task_id, subtask_id, name, "
                           "measurement, quantity, page) VALUES (%(ktd_id)s, %(main_task_id)s, %(summary_task_id)s, "
                           "%(name)s, %(measurement)s, %(quantity)s, %(page)s)", row)
        for i in range(len(self.tables["instrument"])):
            row = self.tables["instrument"].iloc[i].copy()
            row["main_task_id"] = main_task_ids[row["main_task_id"]]
            row["summary_task_id"] = summary_task_ids[row["summary_task_id"]]
            row["subtask_id"] = subtask_ids.get(row["subtask_id"], None)
            cursor.execute("INSERT INTO instrument (ktd_id, main_task_id, summary_task_id, subtask_id, name, "
                           "measurement, quantity, page) VALUES (%(ktd_id)s, %(main_task_id)s, %(summary_task_id)s, "
                           "%(subtask_id)s, %(name)s, %(measurement)s, %(quantity)s, %(page)s)", row)
        self.connection.commit()

    def get_ktd_list(self) -> None:
        """Get a list of KTDs stored in the database"""
        if not self.connection:
            raise KTDParserError("No connection to the database")
        cursor = self.connection.cursor()
        cursor.execute("SELECT id FROM ktd")
        return [row[0] for row in cursor.fetchall()]

    def save_to_file(self, path: str, file_type: Optional[str] = "csv",
                     ktd_id: Optional[str] = None, from_db: Optional[bool] = True) -> None:
        """Save KTD data to excel/csv file.

        Args:
            path: The file path where the data will be saved.
            file_type: The type of file to save the data to ("csv"/"excel")
            ktd_id: KTD id (used when from_db is True). The last saved by default.
            from_db: Whether the data should be retrieved from a database

        Raises:
            KTDParserError: If No connection to the database or no parsed data or invalid file_type value
        """
        if not from_db:
            if self.tables:
                for table, df in self.tables.items():
                    if file_type == "excel":
                        df.to_excel(f"{path}/{table}.xlsx")
                    elif file_type == "csv":
                        df.to_csv(f"{path}/{table}.csv")
                    else:
                        raise KTDParserError("invalid file_type")
                return
            else:
                raise KTDParserError("no parsed data")
        if not self.connection:
            raise KTDParserError("No connection to the database")
        cursor = self.connection.cursor()
        ktd_id = ktd_id or self.ktd_id
        if not ktd_id:
            cursor.execute("SELECT id FROM ktd ORDER BY id DESC LIMIT 1")
            row = cursor.fetchone()
            if row and row[0]:
                ktd_id = row[0]
            else:
                raise KTDParserError("invalid ktd_id")
        table_data = {
            "ktd": {"columns": ("id", "name", "page_count"), "query": f"id = '{ktd_id}'"},
            "main_task": {"columns": ("ktd_id", "id", "name", "page"), "query": f"ktd_id = '{ktd_id}'"},
            "summary_task": {"columns": ("main_task_id", "id", "code", "object", "name", "docs", "profession",
                                         "category", "quantity", "page"),
                             "query": f"main_task_id IN (SELECT id FROM main_task WHERE ktd_id = '{ktd_id}')"},
            "subtask": {"columns": ("ktd_id", "main_task_id", "summary_task_id", "id", "name", "page"),
                        "query": f"ktd_id = '{ktd_id}'"},
            "material": {"columns": ("ktd_id", "main_task_id", "summary_task_id", "subtask_id", "id", "name",
                                     "measurement", "quantity", "page"),
                         "query": f"ktd_id = '{ktd_id}'"},
            "instrument": {"columns": ("ktd_id", "main_task_id", "summary_task_id", "subtask_id", "id", "name",
                                       "measurement", "quantity", "page"),
                           "query": f"ktd_id = '{ktd_id}'"},
            "object": {"columns": ("ktd_id", "main_task_id", "code", "name", "page"), "query": f"ktd_id = '{ktd_id}'"}
        }
        for table in ("ktd", "instrument", "main_task", "material", "object", "subtask", "summary_task"):
            query = f"SELECT {','.join(table_data[table]['columns'])} FROM {table} WHERE {table_data[table]['query']}"
            cursor.execute(query)
            rows = cursor.fetchall()
            df = pd.DataFrame(rows, columns=table_data[table]["columns"])
            if file_type == "excel":
                df.to_excel(f"{path}/{table}.xlsx")
            elif file_type == "csv":
                df.to_csv(f"{path}/{table}.csv")
            else:
                raise KTDParserError("invalid file_type")

    def _parse_file_structure(self) -> None:
        """Analyze file structure"""
        sections = []
        section = None
        with open(self.file_path, "rb") as file:
            reader = PdfReader(file)
            self.page_count = len(reader.pages)
            for page_num in tqdm(range(1, self.page_count + 1), desc="Analyzing file structure",
                                 disable=self.tqdm_disable):
                page = reader.pages[page_num - 1]
                text = page.extract_text()
                if self.PATTERNS["form_title1"].match(text):
                    if section:
                        sections.append(section)
                    section = {
                        "main_task_page": page_num,
                        "forms": [],
                    }
                elif self.PATTERNS["form_title2"].match(text):
                    self.ktd_page = page_num
                elif section is not None:
                    if self.PATTERNS["form_name1"].match(text):
                        section["forms"].append([page_num, None])
                    elif self.PATTERNS["form_name2"].match(text):
                        section["forms"][-1][1] = page_num
        if section:
            sections.append(section)
        self.sections = sections

    def _parse_ktd_page(self) -> str:
        """Parse KTD page"""
        if self.ktd_page:
            page_data = tabula.read_pdf(self.file_path, pages=self.ktd_page, silent=True)[0]
            ktd_id = page_data.columns[1]
            new_row = {"id": ktd_id, "name": page_data.values[4, 1], "page_count": self.page_count}
            self.tables["ktd"] = pd.concat([self.tables["ktd"], pd.DataFrame([new_row])], ignore_index=True)
        elif self.sections and self.sections[0]["main_task_page"]:
            page_data = tabula.read_pdf(self.file_path, pages=self.sections[0]["main_task_page"], silent=True)[0]
            try:
                self.page_offset = int(page_data.values[-1, -1]) - 1
            except (TypeError, ValueError):
                pass
            ktd_id = page_data.columns[1]
            new_row = {"id": ktd_id, "name": page_data.values[4, 1], "page_count": self.page_count}
            self.tables["ktd"] = pd.concat([self.tables["ktd"], pd.DataFrame([new_row])], ignore_index=True)
        else:
            raise KTDParserError("Title page not found")
        return ktd_id

    def _parse_sections(self, ktd_id: str) -> None:
        """Parse file sections"""
        sections_count = len(self.sections)
        for i, section in enumerate(self.sections, 1):
            main_task_id = self._parse_main_task_page(section["main_task_page"], ktd_id)
            for (start, end) in tqdm(section["forms"], desc=f"Section {i}/{sections_count}: Parse form",
                                     disable=self.tqdm_disable):
                try:
                    summary_tasks = self._parse_form(start, end)
                except Exception as e:
                    log_msg(self.logger, logging.ERROR, "Error occurred: %s", e)
                    print(f"The form on pages {start}-{end} has been skipped. "
                          "For more information, please see the log.")
                else:
                    for summary_task in summary_tasks:
                        self._save_summary_task(summary_task, ktd_id, main_task_id)

    def _parse_sections_parallel(self, ktd_id: str, workers: int) -> None:
        """Parse file sections in parallel"""

        def parse_form_parallel(start: int, end: int) -> list:
            """Parse form in parallel"""
            try:
                return self._parse_form(start, end)
            except Exception as e:
                log_msg(self.logger, logging.ERROR, "Error occurred: %s", e)
                print(f"Error occurred on pages {start}-{end}: {e}")

        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
            futures = []
            future_proxy_mapping = {}
            for section in self.sections:
                main_task_id = self._parse_main_task_page(section["main_task_page"], ktd_id)
                for (start, end) in section["forms"]:
                    future = executor.submit(parse_form_parallel, start, end)
                    future_proxy_mapping[future] = (main_task_id, start, end)
                    futures.append(future)
            for future in concurrent.futures.as_completed(futures):
                main_task_id, start, end = future_proxy_mapping[future]
                summary_tasks = future.result()
                for summary_task in summary_tasks:
                    self._save_summary_task(summary_task, ktd_id, main_task_id)

    def _parse_main_task_page(self, page_num: int, ktd_id: str) -> int:
        """Parse main task page"""
        page_data = tabula.read_pdf(self.file_path, pages=page_num, silent=True)[0]
        main_task_id = len(self.tables["main_task"]) + 1
        new_row = {"ktd_id": ktd_id, "id": main_task_id, "name": page_data.values[15, 1], "page": page_num}
        self.tables["main_task"] = pd.concat([self.tables["main_task"], pd.DataFrame([new_row])], ignore_index=True)
        return main_task_id

    def _parse_form(self, start: int, end: int) -> list:
        """Parse section form"""
        summary_tasks = []
        summary_task = {}
        last_row_type = None
        last_object = None
        last_subtask_name = None
        for _page in range(start, end + 1):
            page = _page + self.page_offset
            if _page == start:
                area = [self.FORM_AREA_TOP[0], 0, 100, 100]
            else:
                area = [self.FORM_AREA_TOP[1], 0, 100, 100]
            page_data = tabula.read_pdf(self.file_path, pages=_page, stream=True, relative_area=True, area=area,
                                        columns=self.FORM_COLUMNS_AREA_SUBTASK, pandas_options={"header": None},
                                        silent=True)
            page_data_summary_task = None
            page_data_object = None
            if not page_data:
                log_msg(self.logger, logging.WARNING, "Page %d - Skip page - invalid table format", page)
                if summary_task:
                    summary_tasks.append(summary_task)
                summary_task = {}
                last_row_type = None
                last_object = None
            page_data = page_data[0].replace(float("nan"), None)
            page_data[0] = page_data[0].map(lambda row: re.sub(r"\d", "", str(row).strip()) if row else None)
            if set(page_data[0]) & {"А", "A", "Л"} or last_row_type in ("А", "A", "Л"):
                page_data_summary_task = tabula.read_pdf(self.file_path, pages=_page, stream=True, relative_area=True,
                                                         area=area, columns=self.FORM_COLUMNS_AREA_SUMMARY_TASK,
                                                         pandas_options={"header": None}, silent=True)
                page_data_summary_task = page_data_summary_task[0].replace(float("nan"), None)
            if set(page_data[0]) & {"В", "B"}:
                page_data_object = tabula.read_pdf(self.file_path, pages=_page, stream=True, relative_area=True,
                                                   area=area, columns=self.FORM_COLUMNS_AREA_OBJECT,
                                                   pandas_options={"header": None}, silent=True)
                page_data_object = page_data_object[0].replace(float("nan"), None)
            for i, row in enumerate(page_data.values):
                if (i < 5 and any(map(lambda pattern: row[1] and pattern.match(row[1]), self.PATTERNS["headers"]))) or \
                        row[0] in ("МК", "ВОК"):
                    continue
                elif not any(row):
                    last_row_type = None
                    continue
                row_type = row[0]
                if row_type in ("В", "B"):
                    last_object = {"code": str(page_data_object[1][i]), "name": page_data_object[2][i], "page": page}
                elif row_type in ("А", "A", "Л"):
                    if summary_task:
                        summary_tasks.append(summary_task)
                    summary_task = {
                        "code": page_data_summary_task[2][i],
                        "name": page_data_summary_task[3][i],
                        "docs": page_data_summary_task[4][i].split(";") if page_data_summary_task[4][i] else [],
                        "prof": [],
                        "page": page,
                        "subtask": [],
                        "material": [],
                        "instrument": [],
                        "object": last_object
                    }
                    last_subtask_name = None
                    if last_object:
                        last_object = None
                    if row_type in ("А", "A") and page_data_summary_task[4][i]:
                        page_data_summary_task = self._process_prof_data(page_data_summary_task, i)
                        summary_task["prof"].append([
                            page_data_summary_task[5][i],
                            page_data_summary_task[6][i],
                            page_data_summary_task[7][i]
                        ])
                    last_row_type = row_type
                elif summary_task:
                    if row_type in ("О", "O"):
                        summary_task["subtask"].append({"name": row[1], "page": page})
                        last_subtask_name = row[1]
                        last_row_type = row_type
                    elif row_type in ("Т", "T"):
                        summary_task["instrument"].append({"name": row[1], "subtask_name": last_subtask_name,
                                                           "measurement": row[2], "quantity": row[3], "page": page})
                        last_row_type = row_type
                    elif row_type in ("M", "М", "K", "К"):
                        if last_subtask_name is None:
                            summary_task["material"].append({"name": row[1], "measurement": row[2],
                                                             "subtask_name": None, "quantity": row[3], "page": page})
                        else:
                            summary_task["material"].append({"name": row[1], "measurement": row[2],
                                                             "subtask_name": last_subtask_name, "quantity": row[3],
                                                             "page": page})
                        last_row_type = row_type
                    elif last_row_type and row_type is None:
                        if last_row_type in ("О", "O") and row[1]:
                            summary_task["subtask"][-1]["name"] += " " + row[1]
                            last_subtask_name += " " + row[1]
                        elif last_row_type in ("А", "A", "Л") and (page_data_summary_task[3][i] or
                                                                   page_data_summary_task[4][i] or
                                                                   page_data_summary_task[5][i]) \
                                and not page_data_summary_task[1][i]:
                            if page_data_summary_task[3][i]:
                                summary_task["name"] += " " + page_data_summary_task[3][i]
                            if page_data_summary_task[4][i]:
                                summary_task["docs"].extend(page_data_summary_task[4][i].split(";"))
                            page_data_summary_task = self._process_prof_data(page_data_summary_task, i)
                            if page_data_summary_task[5][i] and not page_data_summary_task[6][i] and \
                                    not page_data_summary_task[7][i]:
                                if summary_task["prof"]:
                                    summary_task["prof"][-1][0] += " " + page_data_summary_task[5][i]
                            elif page_data_summary_task[5][i]:
                                summary_task["prof"].append([
                                    page_data_summary_task[5][i],
                                    page_data_summary_task[6][i],
                                    page_data_summary_task[7][i]
                                ])
                    else:
                        log_msg(self.logger, logging.WARNING, "Page %d - Skip row %d - Invalid row type %s (row: %s)",
                                page, i, str(row_type), row)
                        last_row_type = None
                else:
                    log_msg(self.logger, logging.WARNING, "Page %d - Skip row %d - No summary_task (row: %s)", page, i,
                            row)
        if summary_task and self.tables:
            summary_tasks.append(summary_task)
        return summary_tasks

    def _process_prof_data(self, page_data: pd.DataFrame, row: int) -> pd.DataFrame:
        """Check prof's name and category"""
        if page_data[5][row] and self.PATTERNS["prof"].match(page_data[5][row]) or page_data[6][row] and \
                not page_data[6][row].isnumeric():
            prof_string = "".join([page_data[5][row] or "", page_data[6][row] or ""])
            match = self.PATTERNS["prof"].match(prof_string)
            if match:
                page_data[5][row] = match.group(1)
                page_data[6][row] = match.group(2)
            else:
                page_data[5][row] = prof_string
                page_data[6][row] = None
        return page_data

    def _create_dataframes(self) -> None:
        """Create dataframes"""
        if "ktd" not in self.tables:
            self.tables["ktd"] = pd.DataFrame(columns=["id", "name", "page_count"])
            self.tables["ktd"].astype(dtype={"id": "object", "name": "object", "page_count": "int64"})
        if "main_task" not in self.tables:
            self.tables["main_task"] = pd.DataFrame(columns=["ktd_id", "id", "name", "page"])
            self.tables["main_task"].astype(dtype={"ktd_id": "object", "id": "int64", "name": "object",
                                                   "page": "int64"})
        if "summary_task" not in self.tables:
            self.tables["summary_task"] = pd.DataFrame(columns=["main_task_id", "id", "code", "object", "name", "docs",
                                                                "profession", "category", "quantity", "page"])
            self.tables["summary_task"].astype(dtype={"main_task_id": "int64", "id": "int64", "code": "object",
                                                      "object": "object", "name": "object", "profession": "object",
                                                      "category": "int64", "quantity": "int64", "page": "int64"})
        if "subtask" not in self.tables:
            self.tables["subtask"] = pd.DataFrame(columns=["ktd_id", "main_task_id", "summary_task_id", "id", "name",
                                                           "page"])
            self.tables["subtask"].astype(dtype={"ktd_id": "object", "main_task_id": "int64",
                                                 "summary_task_id": "int64", "id": "int64", "name": "object",
                                                 "page": "int64"})
        if "material" not in self.tables:
            self.tables["material"] = pd.DataFrame(columns=["ktd_id", "main_task_id", "summary_task_id", "subtask_id",
                                                            "id", "name", "measurement", "quantity", "page"])
            self.tables["material"].astype(dtype={"ktd_id": "object", "main_task_id": "int64",
                                                  "summary_task_id": "int64", "subtask_id": "int64", "id": "int64",
                                                  "name": "object", "measurement": "object", "quantity": "float64",
                                                  "page": "int64"})
        if "instrument" not in self.tables:
            self.tables["instrument"] = pd.DataFrame(columns=["ktd_id", "main_task_id", "summary_task_id", "subtask_id",
                                                              "id", "name", "measurement", "quantity", "page"])
            self.tables["instrument"].astype(dtype={"ktd_id": "object", "main_task_id": "int64",
                                                    "summary_task_id": "int64", "subtask_id": "int64", "id": "int64",
                                                    "name": "object", "measurement": "object", "quantity": "int64",
                                                    "page": "int64"})
        if "object" not in self.tables:
            self.tables["object"] = pd.DataFrame(columns=["ktd_id", "main_task_id", "code", "name", "page"])
            self.tables["object"].astype(dtype={"ktd_id": "object", "main_task_id": "int64", "code": "object",
                                                "name": "object", "page": "int64"})

    def _save_summary_task(self, summary_task: int, ktd_id: str, main_task_id: int) -> None:
        """Add summary task data into dataframes"""
        object_code = None
        subtasks = {}
        if summary_task["object"]:
            object_code = str(summary_task["object"]["code"])
            object_row = {"ktd_id": ktd_id, "main_task_id": main_task_id, "code": object_code,
                          "name": summary_task["object"]["name"], "page": summary_task["object"]["page"]}
            self.tables["object"] = pd.concat([self.tables["object"], pd.DataFrame([object_row])],
                                              ignore_index=True)
        if len(self.tables["summary_task"]):
            summary_task_id = self.tables["summary_task"].iloc[-1]["id"] + 1
        else:
            summary_task_id = 1
        summary_task_row = {"main_task_id": main_task_id, "id": summary_task_id, "code": str(summary_task["code"]),
                            "name": summary_task["name"], "object": object_code,
                            "docs": ";".join([doc.strip() for doc in summary_task["docs"]]),
                            "profession": None, "category": None, "quantity": None, "page": summary_task["page"]}
        if summary_task["prof"]:
            for prof in summary_task["prof"]:  # Duplication with different professions
                summary_task_row["profession"], summary_task_row["category"], summary_task_row["quantity"] = prof
                self.tables["summary_task"] = pd.concat([self.tables["summary_task"], pd.DataFrame([summary_task_row])],
                                                        ignore_index=True)
        else:
            self.tables["summary_task"] = pd.concat([self.tables["summary_task"], pd.DataFrame([summary_task_row])],
                                                    ignore_index=True)
        for subtask in summary_task["subtask"]:
            subtask_id = len(self.tables["subtask"]) + 1
            subtasks[subtask["name"]] = subtask_id
            subtask_row = {"ktd_id": ktd_id, "main_task_id": main_task_id, "summary_task_id": summary_task_id,
                           "id": subtask_id, "name": subtask["name"], "page": subtask["page"]}
            self.tables["subtask"] = pd.concat([self.tables["subtask"], pd.DataFrame([subtask_row])],
                                               ignore_index=True)
        for material in summary_task["material"]:
            material_id = len(self.tables["material"]) + 1
            subtask_id = subtasks.get(material["subtask_name"], None)
            material_row = {"ktd_id": ktd_id, "main_task_id": main_task_id, "summary_task_id": summary_task_id,
                            "subtask_id": subtask_id, "id": material_id, "name": material["name"],
                            "measurement": material["measurement"], "quantity": material["quantity"],
                            "page": material["page"]}
            self.tables["material"] = pd.concat([self.tables["material"], pd.DataFrame([material_row])],
                                                ignore_index=True)
        for instrument in summary_task["instrument"]:
            instrument_id = len(self.tables["subtask"]) + 1
            subtask_id = subtasks.get(instrument["subtask_name"], 0)
            instrument_row = {"ktd_id": ktd_id, "main_task_id": main_task_id, "summary_task_id": summary_task_id,
                              "subtask_id": subtask_id, "id": instrument_id, "name": instrument["name"],
                              "measurement": instrument["measurement"], "quantity": instrument["quantity"],
                              "page": instrument["page"]}
            self.tables["instrument"] = pd.concat([self.tables["instrument"], pd.DataFrame([instrument_row])],
                                                  ignore_index=True)
        log_msg(self.logger, logging.INFO, "Ktd %s - Main task %d - Summary task %d saved", ktd_id, main_task_id,
                summary_task_id)
