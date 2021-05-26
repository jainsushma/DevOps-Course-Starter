"""Unit tests for view_model.py"""
import pytest
from todo_app.view_model import ViewModel
from todo_app.item import Item

def test_todo_items():
    items = [
                Item(1, "Test_ToDo1", "to-do"),
            ]
    todo_items_list = ViewModel(items).todo_items
    assert len(todo_items_list) > 0, "No ToDo item found"

def test_doing_items():
    items = [
                Item(1, "Test_Doing1", "doing"),
            ]
    doing_items_list = ViewModel(items).doing_items
    assert len(doing_items_list) > 0, "No Doing item found"

def test_done_items():
    items = [
                Item(1, "Test_Done1", "done"),
            ]
    done_items_list = ViewModel(items).done_items
    assert len(done_items_list) > 0, "No Done item found"
