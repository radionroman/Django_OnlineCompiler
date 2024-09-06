Here’s a `README.md` for your Django project:

---

# C-to-Assembler Compiler Web App

This Django project is a web-based platform that allows users to upload a C file, select a compiler, compile the C file into assembly language, and view the resulting assembler code alongside the original C code.

## Features

- **File Upload:** Upload a C file (.c) through the web interface.
- **Compiler Selection:** Choose from different C compilers (GCC, Clang, etc.).
- **C to Assembly Translation:** Compile the uploaded C file into assembly language using the selected compiler.
- **Side-by-Side Viewer:** View the C code alongside the corresponding assembly code, line by line.

## Requirements

Before you begin, ensure you have the following installed:

- Python 3.x
- Django 3.x or later
- GCC, Clang, or other C compilers
- Linux/macOS/WSL (for running compilers)
  
### Python Dependencies:

Install the required Python packages using:

```bash
pip install -r requirements.txt
```

## Installation and Setup

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd <project-directory>
   ```

2. **Install dependencies**:

   Make sure you have `pip` installed. Run the following command to install the necessary Python packages:

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the compilers**:

   The app allows users to choose between different compilers like GCC and Clang. Ensure these compilers are installed on your machine and accessible via the command line. You can modify the available compilers in the Django project’s settings file.

4. **Apply migrations**:

   ```bash
   python manage.py migrate
   ```

5. **Start the Django development server**:

   ```bash
   python manage.py runserver
   ```

6. **Access the app**:

   Open your web browser and navigate to `http://127.0.0.1:8000/` to access the app.

## How It Works

1. **Upload a C file**: Use the provided form to upload a `.c` file.
2. **Choose a compiler**: Select the compiler you want to use for translation.
3. **Compile the code**: The app will compile the C file and generate the corresponding assembly code.
4. **View results**: View the original C code and the compiled assembly code side by side.


## Compilers

By default, this project supports the following compilers:

- **GCC** (GNU Compiler Collection)
- **Clang**

You can modify the available compilers or add new ones in the `settings.py` file.

## License

This project is licensed under the MIT License.

## Contributions

Feel free to contribute to the project by submitting issues or pull requests!
