# CSV2IR

**By [Douwe den Blanken](https://nl.linkedin.com/in/douwedenblanken) ([v0xnihili](https://github.com/V0XNIHILI/))**

This repository contains the `Csv2ir.py` script, which can convert all CSV files in a folder to
infrared images into another folder.

## 📃 Requirements

Please make sure that you have `numpy` installed.

Also install the `pypng` package, needed for creating the infrared PNG images, by running the
following command:

```
pip install pypng
```

## 🎯 How to run

### Easy way

First, make a new folder in the current folder: call it 'csv'. Then, put all of your CSV files into
that folder. Finally, execute the Csv2ir.py file.

### Developer way

First, `cd` into the project's root directory and run `chmod +x Csv2ir.py`. Then, to actually
convert the CSV files to images, run: `Csv2ir input_folder_name output_folder_name`, where you
replace `input_folder_name` and `output_folder_name` by their actual values.

## 🚀 How fast is it?

I tried my best to make the program as fast as possible. On eight processing cores, the program
needs 1 minute and 9 seconds to process 506 images; in other words, 0.136 seconds per image.
