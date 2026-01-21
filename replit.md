# Lightning Network Routing Tutorial

## Overview
An interactive online textbook with Rust coding exercises to teach developers how Bitcoin's Lightning Network Routing works.

## Project Structure
- `app.py` - Flask backend server that serves tutorials and compiles/runs Rust code
- `templates/` - HTML templates for the web interface
  - `index.html` - Home page with chapter listing
  - `tutorial.html` - Individual tutorial page with code editor
- `static/` - CSS styles
  - `style.css` - Dark theme styling

## How It Works
1. Users navigate through tutorial chapters
2. Each chapter has explanatory content and a Rust code exercise
3. Users can write Rust code in the built-in editor
4. Code is compiled and executed on the server using `rustc`
5. Output is displayed back to the user

## Adding New Tutorials
Edit the `TUTORIALS` list in `app.py` to add new chapters:
```python
{
    "id": 4,
    "title": "Your Tutorial Title",
    "content": "<p>HTML content for the tutorial...</p>",
    "code": 'fn main() {\n    // Starter code\n}'
}
```

## Running the Application
The application runs on port 5000 using Flask.

## Recent Changes
- January 21, 2026: Initial project setup with blank tutorial structure
