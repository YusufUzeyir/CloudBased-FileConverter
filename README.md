# docxtopdf

This repository contains a Python function to convert DOCX files to PDF format.

**Note:** This function is currently designed for use on Windows operating systems.

## Functionality

The `docxtopdf` function handles the conversion process as follows:

1. **Checks request method:** Ensures the request is a POST method.
2. **Initialization:** Initializes the `pythoncom` library for working with COM objects (required for Windows interaction with Microsoft Word).
3. **File handling:**
   - Generates a unique identifier (`file_id`) using `uuid.uuid4()`.
   - Creates temporary filenames for the uploaded DOCX and converted PDF files using the generated `file_id`.
   - Retrieves the uploaded DOCX file from the request object (`request.FILES['docx']`).
   - Saves the uploaded DOCX file to the temporary location.
4. **Conversion:** Calls the `convert` function (implementation assumed to be elsewhere) to perform the DOCX to PDF conversion using the temporary filenames.
5. **PDF response:**
   - Reads the converted PDF content from the temporary file.
   - Creates an HTTP response object with the PDF data and appropriate content type (`application/pdf`).
   - Sets the content disposition header to allow inline display (`inline`) and specify the filename for download (`converted_{file_id}.pdf`).
6. **Cleanup:** Removes the temporary DOCX and PDF files after successful conversion.
7. **Error handling:** In case of exceptions, returns an HTTP response with an error message.

## Usage

1. **Include the function:** Import the `docxtopdf` function into your application code.
2. **Process upload:** In a view function or similar context, handle the file upload and pass the request object to the `docxtopdf` function.
3. **Handle response:** The function returns an HTTP response object. You can either return this directly or process the response further in your application logic.

## Code Example

```python
def docxtopdf(request):
    if request.method == 'POST':
        pythoncom.CoInitialize()  
        try:
            
            file_id = str(uuid.uuid4())
            docx_filename = f"uploaded_{file_id}.docx" 
            pdf_filename = f"converted_{file_id}.pdf"

            docx_file = request.FILES['docx']

            with open(docx_filename, 'wb') as f:
                f.write(docx_file.read())

            convert(docx_filename, pdf_filename)  

            with open(pdf_filename, 'rb') as f:
                pdf_data = f.read()

            response = HttpResponse(pdf_data, content_type='application/pdf')
            response['Content-Disposition'] = f'inline; filename={pdf_filename}'

            os.remove(docx_filename)
            os.remove(pdf_filename)

            return response
        except Exception as e:
            return HttpResponse(f"An error occurred: {e}")

    return render(request, 'docxtopdf.html')
