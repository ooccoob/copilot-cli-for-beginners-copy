import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from utils import print_menu, get_user_choice, get_book_details, print_books
from books import Book


# ── print_menu ────────────────────────────────────────────────────────────────

def test_print_menu(capsys):
    print_menu()
    captured = capsys.readouterr()
    assert "Book Collection App" in captured.out
    assert "1. Add a book" in captured.out
    assert "5. Exit" in captured.out


# ── get_user_choice ───────────────────────────────────────────────────────────

def test_get_user_choice(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "3")
    assert get_user_choice() == "3"


def test_get_user_choice_strips_whitespace(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "  2  ")
    assert get_user_choice() == "2"


# ── get_book_details ──────────────────────────────────────────────────────────

def test_get_book_details_valid(monkeypatch):
    responses = iter(["Dune", "Frank Herbert", "1965"])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))
    title, author, year = get_book_details()
    assert title == "Dune"
    assert author == "Frank Herbert"
    assert year == 1965


def test_get_book_details_invalid_year_defaults_to_zero(monkeypatch, capsys):
    responses = iter(["1984", "George Orwell", "not-a-year"])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))
    title, author, year = get_book_details()
    assert year == 0
    captured = capsys.readouterr()
    assert "Invalid year" in captured.out


def test_get_book_details_strips_whitespace(monkeypatch):
    responses = iter(["  The Hobbit  ", "  Tolkien  ", "1937"])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))
    title, author, year = get_book_details()
    assert title == "The Hobbit"
    assert author == "Tolkien"


# ── print_books ───────────────────────────────────────────────────────────────

def test_print_books_empty(capsys):
    print_books([])
    captured = capsys.readouterr()
    assert "No books" in captured.out


def test_print_books_unread(capsys):
    books = [Book(title="Dune", author="Frank Herbert", year=1965, read=False)]
    print_books(books)
    captured = capsys.readouterr()
    assert "Dune" in captured.out
    assert "Frank Herbert" in captured.out
    assert "1965" in captured.out
    assert "Unread" in captured.out


def test_print_books_read(capsys):
    books = [Book(title="1984", author="George Orwell", year=1949, read=True)]
    print_books(books)
    captured = capsys.readouterr()
    assert "1984" in captured.out
    assert "Read" in captured.out


def test_print_books_multiple(capsys):
    books = [
        Book(title="Book A", author="Author A", year=2000, read=True),
        Book(title="Book B", author="Author B", year=2001, read=False),
    ]
    print_books(books)
    captured = capsys.readouterr()
    assert "Book A" in captured.out
    assert "Book B" in captured.out
