from daisy_converter import docx_to_daisy
import zipfile
import os

input_docx = "sample.docx"  # Test .docx file path (ensure it exists in your working directory)
output_zip = "sample_daisy.zip"  # Output ZIP package name

# Convert the DOCX to a DAISY 3 package
docx_to_daisy(input_docx, output_zip)
print(f"Converted '{input_docx}' to DAISY 3 book: '{output_zip}'.")

# Verify the contents of the generated ZIP file
if os.path.exists(output_zip):
    with zipfile.ZipFile(output_zip, 'r') as z:
        files = z.namelist()
        print("Files in the ZIP package:")
        for f in files:
            print(" -", f)

        required_files = {"book.xml", "book.ncx", "book.smil", "book.opf"}
        missing = required_files - set(files)
        if missing:
            print("Missing required files:", missing)
        else:
            print("All required files are present.")

        image_files = [f for f in files if f.startswith("images/") and not f.endswith("/")]
        if image_files:
            print("Image files found:", image_files)
        else:
            print("No images found in the package.")
else:
    print("Conversion failed: Output ZIP file not found.")
