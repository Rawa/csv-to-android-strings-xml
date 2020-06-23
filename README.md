# CSV to Android Strings.xml

This projects has a quick solution to generate strings.xml files from a CSV file. It supports normal `<string>` tag and `<plurals>`.

String replacement (e.g $1%s or %d) is not supported, it is expected that they are included in csv.

## Usage

```
usage: Generator.py [-h] -i INPUT_FILE -o OUTPUT_FILE [-k KEY_COLUMN] -v
                    VALUE_COLUMN -p PLURAL_COLUMN [-r START_ROW]

Convert csv to Android localization files

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input INPUT_FILE
                        CSV input file
  -o OUTPUT_FILE, --output OUTPUT_FILE
                        CSV input file
  -k KEY_COLUMN, --key-column KEY_COLUMN
                        Column for keys
  -v VALUE_COLUMN, --value-column VALUE_COLUMN
                        Column for values
  -p PLURAL_COLUMN, --plural-column PLURAL_COLUMN
                        Column for plural values
  -r START_ROW, --start-row START_ROW
                        Row where data starts
```

### Sample

A sample document in Google Sheets can be found [here](https://docs.google.com/spreadsheets/d/15AAEPShRAjhbCZKp7mEQUDyPgreoXRqI9AwUMEGEUxI/edit?usp=sharing) and simply edit and export it to csv and run the following command

` $ ./Generator.py --input example.csv --output strings.xml --key-column 0 --plural-column 1 --value-column 3 --start-row 1 `

This will yeild the following output

```xml
<?xml version="1.0" ?>
<resources>
    <plurals name="main_fragment_bottom_summary">
        <item quantity="zero">No bar dropped</item>
        <item quantity="one">One bar dropped</item>
        <item quantity="other">%d bars dropped</item>
    </plurals>
    <string name="main_fragment_button">Cool Button</string>
    <string name="main_fragment_title">Cool Fragment</string>
    <plurals name="noti_foos_count">
        <item quantity="zero">%d foos</item>
        <item quantity="one">%d foo</item>
        <item quantity="other">%d foos</item>
    </plurals>
    <string name="secondary_fragment_button">Less Cool Button</string>
    <string name="secondary_fragment_title">Less Cool Fragment</string>
</resources>
```
