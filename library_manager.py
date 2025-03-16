import streamlit as st
import requests

API_URL = "http://localhost:8000"  # Replace with FastAPI URL in production

# Helper functions to interact with the backend
def get_books():
    response = requests.get(f"{API_URL}/books/")
    return response.json()

def add_book(book_data):
    response = requests.post(f"{API_URL}/books/", json=book_data)
    return response.json()

def delete_book(book_id):
    response = requests.delete(f"{API_URL}/books/{book_id}")
    return response.json()

def search_books(search_term):
    response = requests.get(f"{API_URL}/books/")
    books = response.json()
    return [book for book in books if search_term.lower() in book["title"].lower() or search_term.lower() in book["author"].lower()]

def get_books_by_status(read_status):
    response = requests.get(f"{API_URL}/books/")
    books = response.json()
    return [book for book in books if book["read"] == read_status]

# Custom styles for Streamlit
st.markdown("""
    <style>
        .title {
            font-size: 40px;
            font-weight: bold;
            color: #5e4b8b;
        }
        .section-header {
            font-size: 30px;
            font-weight: bold;
            color: #8f5c9c;
        }
        .subheader {
            font-size: 20px;
            color: #6b3f73;
        }
        .container {
            background-color: #f9f7f7;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
        }
        .button {
            background-color: #8f5c9c;
            color: white;
            border-radius: 8px;
            padding: 10px 20px;
            font-weight: bold;
            transition: all 0.3s ease;
        }
        .button:hover {
            background-color: #6b3f73;
        }
        .sidebar .sidebar-content {
            font-size: 20px;
            font-weight: bold;
            color: #6b3f73;
        }
        .footer {
            font-size: 18px;
            color: #6b3f73;
            text-align: center;
            margin-top: 20px;
        }
    </style>
""", unsafe_allow_html=True)


st.title("📚 Personal Library Manager", anchor="top")
# Sidebar Customization
st.sidebar.markdown("<h2 style='font-size: 28px; color: #6b3f73;'>Menu</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<hr>", unsafe_allow_html=True)

# Adding a dropdown menu for the sidebar actions
action = st.sidebar.selectbox("Select Action", ["Add Book", "View Books", "Search Book", "Delete Book", "Status Check", "Exit"], index=0, label_visibility="visible")



# Main Page Content Based on Sidebar Selection
if action == "Add Book":
    st.markdown('<div class="container">', unsafe_allow_html=True)
    st.header("📖 Add a New Book", anchor="add-book")
    st.subheader("Fill in the details below to add a new book:")

    # Book information input fields
    title = st.text_input("Title", max_chars=100)
    author = st.text_input("Author", max_chars=100)
    year = st.number_input("Year of Publication", min_value=0, max_value=2025, step=1)
    genre = st.text_input("Genre", max_chars=50)
    read_status = st.radio("Have you read this book?", ("Yes", "No"))
    
    if st.button("Add Book", key="add_book", help="Click to add the book to the library"):
        read_bool = True if read_status == "Yes" else False
        book_data = {
            "title": title,
            "author": author,
            "year": year,
            "genre": genre,
            "read": read_bool
        }
        added_book = add_book(book_data)
        st.success(f"✅ Book '{added_book['title']}' by {added_book['author']} added successfully!")

    st.markdown('</div>', unsafe_allow_html=True)

elif action == "View Books":
    st.markdown('<div class="container">', unsafe_allow_html=True)
    st.header("📚 All Books")
    books = get_books()

    if books:
        for book in books:
            read_status = "✅ Read" if book['read'] else "❌ Unread"
            st.write(f"**{book['title']}** by {book['author']} ({book['year']}) - {read_status}")
    else:
        st.warning("No books available in your library.")
    
    st.markdown('</div>', unsafe_allow_html=True)

elif action == "Search Book":
    st.markdown('<div class="container">', unsafe_allow_html=True)
    st.header("🔍 Search for a Book")
    search_term = st.text_input("Enter title or author to search")
    
    if st.button("Search"):
        if search_term:
            books = search_books(search_term)
            if books:
                for book in books:
                    read_status = "✅ Read" if book['read'] else "❌ Unread"
                    st.write(f"**{book['title']}** by {book['author']} ({book['year']}) - {read_status}")
            else:
                st.warning(f"No books found matching '{search_term}'.")
        else:
            st.warning("Please enter a search term.")
    
    st.markdown('</div>', unsafe_allow_html=True)

elif action == "Delete Book":
    st.markdown('<div class="container">', unsafe_allow_html=True)
    st.header("🗑️ Delete a Book")
    books = get_books()
    
    if books:
        book_titles = [book["title"] for book in books]
        selected_book_title = st.selectbox("Select a book to delete", book_titles)
        
        if st.button("Delete Book", help="Click to delete the selected book"):
            selected_book = next(book for book in books if book["title"] == selected_book_title)
            deleted_book = delete_book(selected_book["id"])
            st.success(f"✅ Book '{deleted_book['title']}' by {deleted_book['author']} deleted successfully!")
    else:
        st.warning("No books available to delete.")
    
    st.markdown('</div>', unsafe_allow_html=True)

elif action == "Status Check":
    st.markdown('<div class="container">', unsafe_allow_html=True)
    st.header("📖 View Books by Status")
    status = st.radio("Select status", ("Read", "Unread"))
    read_status = True if status == "Read" else False
    
    books_by_status = get_books_by_status(read_status)
    
    if books_by_status:
        for book in books_by_status:
            read_status_str = "✅ Read" if book["read"] else "❌ Unread"
            st.write(f"**{book['title']}** by {book['author']} ({book['year']}) - {read_status_str}")
    else:
        st.warning(f"No {status.lower()} books available.")
    
    st.markdown('</div>', unsafe_allow_html=True)

elif action == "Exit":
    st.markdown('<div class="container">', unsafe_allow_html=True)
    st.header("Goodbye! 👋")
    st.write("Thank you for using the Personal Library Manager! Feel free to come back anytime.")
    st.markdown('</div>', unsafe_allow_html=True)


# Name and Social Links
st.markdown("""
    <div style="text-align: center; font-size: 24px; color: #8f5c9c; font-weight: bold;">
        SYED SHOAIB SHERAZI
    </div>
    <div style="text-align: center; font-size: 18px;">
        <a href="https://github.com/your-github" target="_blank" style="color: #6b3f73; text-decoration: none;">GitHub</a> | 
        <a href="https://linkedin.com/in/your-linkedin" target="_blank" style="color: #6b3f73; text-decoration: none;">LinkedIn</a>
    </div>
    <hr style="border: 1px solid #8f5c9c;">
""", unsafe_allow_html=True)