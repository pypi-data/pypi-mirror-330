# **ktdparser**

The **ktdparser** library is designed to extract data from a PDF file containing information about KTD (complex technical documentation). This README briefly describes the functionality and usage of **ktdparser**.

## Installation

To install the **ktdparser** library, follow these steps:

1. Install the required dependencies:
    ```bash
    pip install tabula-py==2.9.0 psycopg2-binary==2.9.9 openpyxl==3.1.2 PyPDF2==3.0.1 tqdm
    ```
2. Install **ktdparser**:
    ```bash
    pip install ktdparser
    ```

## Usage

Here's a simple example of how to use **ktdparser**:

### With database saving
```python
from ktdparser import KTDParser


parser = KTDParser()
parser.connect_to_db(password="password")
parser.parse_pdf("ktd.pdf", log="path/to/log.log", progressbar=True)
parser.save_to_db()
parser.save_to_file()
```

### Without database saving
```python
from ktdparser import KTDParser

parser = KTDParser()
parser.parse_pdf("ktd.pdf", progressbar=True)
parser.save_to_file("/ktd_data", "excel", from_db=False)
```


## Methods

1. **parse_pdf**: Parse the KTD file and save the results.

	Arguments:

	- **file_path**: Path to the PDF file to parse.
	- **progressbar**: Show progress indicator.
	- **log**: Record to log file. If True, log to default location. If False, do not log. If str, specify log file path.
	- **form_top**: Relative distance (%) from the top of the page to the table, excluding table headers on the first page of the form and others. If not specified, defaults to (25, 15).
	- **columns**: X-coordinates of columns (9). If not specified, defaults to (56.07, 94.2, 130.82, 329.66, 522.58, 626.26, 659.23, 722.54, 780.11).
	- **workers**: Number of threads for parallel parsing.

2. **connect_to_db**: Establish connection to the database.

	Arguments:

	- **password**: Password for the database user.
	- **user**: Database user name.
	- **host**: Database host address.
	- **port**: Database port number.
	- **database**: Database name.

3. **save_to_db**: Save data to the database.

4. **save_to_file**: Save data to an Excel/CSV file.

	Arguments:

	- **path**: Path to the file to save data.
	- **file_type**: File type for saving data ("csv" or "excel").
	- **ktd_id**: Identifier of the KTD (used when from_db is True). Defaults to the last saved KTD in the database.
	- **from_db**: Determine whether data should be retrieved from the database or from the tables attribute.

5. **get_ktd_list**: Get a list of all saved KTD identifiers in the database.