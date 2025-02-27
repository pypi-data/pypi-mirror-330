from daisy_converter import docx_to_daisy, check_docx_preparation
import os
import zipfile

# Path to your input DOCX file; ensure that the file exists.
input_docx = "sample.docx"
# Desired output ZIP package name.
output_zip = "sample_daisy.zip"

# 1. Run document preparation checks
print("Running document preparation checks:")
check_docx_preparation(input_docx)
print("-" * 40)

# 2. Convert the DOCX to a DAISY 3 package
docx_to_daisy(input_docx, output_zip)
print(f"Converted '{input_docx}' to DAISY 3 book: '{output_zip}'.")

# 3. Verify the contents of the generated ZIP file
if os.path.exists(output_zip):
    with zipfile.ZipFile(output_zip, 'r') as z:
        files = z.namelist()
        print("\nFiles in the ZIP package:")
        for f in files:
            print(" -", f)

        required_files = {"book.xml", "book.ncx", "book.smil", "book.opf"}
        missing = required_files - set(files)
        if missing:
            print("\nMissing required files:", missing)
        else:
            print("\nAll required files are present.")

        image_files = [f for f in files if f.startswith("images/") and not f.endswith("/")]
        if image_files:
            print("\nImage files found:", image_files)
        else:
            print("\nNo images found in the package.")
else:
    print("Conversion failed: Output ZIP file not found.")
