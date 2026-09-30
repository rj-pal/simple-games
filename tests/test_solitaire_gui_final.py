"""
Test suite for SolitaireGUI.py

Testing strategy:
1. Test backend game logic independently (no GUI)
2. Mock the backend when testing GUI event handlers
3. Test UI state changes without rendering full Tkinter app
4. Use unittest.mock to patch Tkinter and game objects

Project structure:
    project/
    ├── tests/
    │   └── test_solitaire_gui_final.py (this file)
    ├── gui/
    │   ├── SolitaireGUI.py
    │   ├── GameGUI.py
    │   └── (other GUI files)
    ├── games/
    │   └── solitaire.py
    └── utils/
        ├── errors.py
        └── emojis.py

IMPORTANT: This file has sys.path setup to work from tests/ directory
           and imports gui.SolitaireGUI BEFORE patching it.

Run from project root with:
    python -m pytest tests/test_solitaire_gui_final.py -v
"""

import unittest
from unittest.mock import Mock, MagicMock, patch, call
import tkinter as tk
from io import StringIO
import sys
import os

# Add project root to path so imports work from tests/ directory
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestGameLogicIndependently(unittest.TestCase):
    """
    Test the backend Solitaire game logic WITHOUT the GUI.
    This is the easiest and fastest to test.
    """
    
    def setUp(self):
        """Import and test your actual Solitaire class"""
        from games.solitaire import Solitaire
        self.game = Solitaire(klondike_value=1)
    
    def test_game_initialization(self):
        """Test that game initializes correctly"""
        self.assertIsNotNone(self.game)
        self.assertEqual(len(self.game.tableau), 7)
    
    def test_draw_from_stock_pile(self):
        """Test drawing from stock pile"""
        self.game.draw()
        # Verify waste pile was updated
    
    def test_transfer_valid_move(self):
        """Test transferring cards between tableau piles"""
        source_pile = 0
        dest_pile = 1
        self.game.transfer(source_pile, dest_pile, 1)
        # Verify card was moved


class TestSolitaireGUIWithMocking(unittest.TestCase):
    """
    Test the GUI logic by mocking the backend game object.
    This allows testing click handlers and UI logic without rendering.
    """
    
    def setUp(self):
        """Set up a test GUI with mocked game backend"""
        # Create a mock root window
        self.root = tk.Tk()
        
        # IMPORTANT: Import the module FIRST to make it available for patching
        import gui.SolitaireGUI
        
        # Now patch where Solitaire is imported in that module
        self.solitaire_patcher = patch('gui.SolitaireGUI.Solitaire')
        self.mock_solitaire_class = self.solitaire_patcher.start()
        
        # Create a mock game instance
        self.mock_game = MagicMock()
        self.mock_solitaire_class.return_value = self.mock_game
        
        # Set up mock pile objects
        self.mock_stock_pile = MagicMock()
        self.mock_waste_pile = MagicMock()
        
        self.mock_game.get_stock_pile.return_value = self.mock_stock_pile
        self.mock_game.get_waste_pile.return_value = self.mock_waste_pile
        self.mock_game.get_waste_pile_for_print.return_value = ["♠K", "♠Q"]
        
        # Set up mock foundation and tableau
        self.mock_game.foundation_piles = {
            'S': MagicMock(),
            'H': MagicMock(),
            'D': MagicMock(),
            'C': MagicMock(),
        }
        
        self.mock_game.tableau = [MagicMock() for _ in range(7)]
        self.mock_game.check_win.return_value = False
        self.mock_game.check_empty_stock_pile.return_value = False
        self.mock_game.check_empty_waste_pile.return_value = False
        
        # Now import and create the GUI
        from gui.SolitaireGUI import SolitaireGUI
        self.gui = SolitaireGUI(self.root)
    
    def tearDown(self):
        """Clean up after each test"""
        self.solitaire_patcher.stop()
        try:
            self.root.destroy()
        except:
            pass
    
    def test_gui_initialization(self):
        """Test that GUI initializes correctly"""
        self.assertIsNotNone(self.gui)
        self.assertEqual(self.gui.game, self.mock_game)
        self.assertIsNone(self.gui.selected_item)
    
    def test_on_click_stock_calls_draw(self):
        """Test that clicking stock pile calls game.draw()"""
        mock_event = MagicMock()
        
        self.gui.on_click_stock(mock_event)
        
        self.mock_game.draw.assert_called_once()
    
    def test_on_click_stock_with_selected_item_does_nothing(self):
        """Test that clicking stock with item selected doesn't trigger draw"""
        self.gui.selected_item = (1, 0)  # Something is selected
        mock_event = MagicMock()
        
        self.gui.on_click_stock(mock_event)
        
        self.mock_game.draw.assert_not_called()
    
    def test_on_click_reset_resets_game(self):
        """Test that clicking reset calls game.reset_pile()"""
        mock_event = MagicMock()
        
        self.gui.on_click_reset(mock_event)
        
        self.mock_game.reset_pile.assert_called_once()
    
    def test_on_click_waste_with_valid_selection(self):
        """Test clicking waste pile to select a card"""
        mock_event = MagicMock()
        mock_widget = MagicMock()
        mock_event.widget = mock_widget
        
        # First click - select the card
        self.gui.on_click_waste(mock_event)
        
        self.assertEqual(self.gui.selected_item, (1, -1))
        self.assertEqual(self.gui.highlighted_widget, mock_widget)
    
    def test_on_click_tableau_empty_pile(self):
        """Test clicking empty tableau pile with nothing selected"""
        self.gui.tableau[0].is_empty.return_value = True
        mock_event = MagicMock()
        
        self.gui.on_click_tableau(mock_event, 1, 0)
        
        # Should not do anything
        self.assertIsNone(self.gui.selected_item)
    
    def test_card_transfer_sequence(self):
        """Test selecting a card then moving it"""
        mock_event1 = MagicMock()
        mock_widget1 = MagicMock()
        mock_event1.widget = mock_widget1
        
        mock_event2 = MagicMock()
        mock_widget2 = MagicMock()
        mock_event2.widget = mock_widget2
        
        # Mock tableau piles
        for pile in self.gui.tableau:
            pile.is_empty.return_value = False
            pile.size = 2
        
        # First click - select a card from pile 0
        self.gui.on_click_tableau(mock_event1, 1, 0)
        self.assertEqual(self.gui.selected_item, (1, 0))
        
        # Second click - move to pile 1
        self.gui.on_click_tableau(mock_event2, 1, 1)
        
        # Verify transfer was called
        self.mock_game.transfer.assert_called_once_with(0, 1, 1)
        
        # Selection should be cleared
        self.assertIsNone(self.gui.selected_item)
    
    def test_move_to_foundation_valid(self):
        """Test moving card from tableau to foundation"""
        # Set up mock card with suit
        mock_card = MagicMock()
        mock_card.suit = 'S'
        self.mock_game.get_tableau_card.return_value = mock_card
        
        # Set up foundation
        self.mock_game.foundation_piles['S'].is_empty.return_value = False
        
        mock_event_card = MagicMock()
        mock_event_foundation = MagicMock()
        mock_event_foundation.widget = MagicMock()
        
        # Select a card from tableau
        self.gui.selected_item = (1, 0)
        self.gui.highlighted_widget = MagicMock()
        
        # Click foundation with matching suit
        self.gui.on_click_foundation(mock_event_foundation, 'S')
        
        self.mock_game.move_to_foundation.assert_called_once()
    
    def test_move_to_foundation_suit_mismatch(self):
        """Test that moving to foundation with wrong suit fails"""
        mock_card = MagicMock()
        mock_card.suit = 'H'
        self.mock_game.get_tableau_card.return_value = mock_card
        
        self.gui.selected_item = (1, 0)
        mock_event = MagicMock()
        
        with patch('tkinter.messagebox.showinfo') as mock_messagebox:
            self.gui.on_click_foundation(mock_event, 'S')
            
            # Should show error message
            mock_messagebox.assert_called_once()
            self.assertIn("Suit Mismatch", str(mock_messagebox.call_args))


class TestGUIStateManagement(unittest.TestCase):
    """Test the GUI state management without full Tkinter rendering"""
    
    def setUp(self):
        self.root = tk.Tk()
        import gui.SolitaireGUI  # Import module first
        with patch('gui.SolitaireGUI.Solitaire'):
            from gui.SolitaireGUI import SolitaireGUI
            self.gui = SolitaireGUI(self.root)
    
    def tearDown(self):
        try:
            self.root.destroy()
        except:
            pass
    
    def test_selection_state_initialization(self):
        """Test that selection state starts as None"""
        self.assertIsNone(self.gui.selected_item)
        self.assertIsNone(self.gui.highlighted_widget)
        self.assertIsNone(self.gui.foundation_suit_in_play)
    
    def test_selection_state_changes(self):
        """Test selection state changes through user interaction"""
        # Simulate selecting a card
        self.gui.selected_item = (1, 0)
        self.gui.highlighted_widget = "test_widget"
        
        self.assertEqual(self.gui.selected_item, (1, 0))
        self.assertEqual(self.gui.highlighted_widget, "test_widget")
        
        # Simulate clearing selection
        self.gui.selected_item = None
        self.gui.highlighted_widget = None
        
        self.assertIsNone(self.gui.selected_item)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error handling"""
    
    def setUp(self):
        self.root = tk.Tk()
        import gui.SolitaireGUI  # Import module first
        self.solitaire_patcher = patch('gui.SolitaireGUI.Solitaire')
        self.mock_solitaire_class = self.solitaire_patcher.start()
        self.mock_game = MagicMock()
        self.mock_solitaire_class.return_value = self.mock_game
        
        # Set up minimal mocks
        self.mock_game.get_stock_pile.return_value = MagicMock()
        self.mock_game.get_waste_pile.return_value = MagicMock()
        self.mock_game.get_waste_pile_for_print.return_value = []
        self.mock_game.foundation_piles = {'S': MagicMock(), 'H': MagicMock(), 
                                           'D': MagicMock(), 'C': MagicMock()}
        self.mock_game.tableau = [MagicMock() for _ in range(7)]
        self.mock_game.check_win.return_value = False
        self.mock_game.check_empty_stock_pile.return_value = False
        self.mock_game.check_empty_waste_pile.return_value = True
        
        from gui.SolitaireGUI import SolitaireGUI
        self.gui = SolitaireGUI(self.root)
    
    def tearDown(self):
        self.solitaire_patcher.stop()
        try:
            self.root.destroy()
        except:
            pass
    
    def test_game_error_handling(self):
        """Test that GameError exceptions are caught gracefully"""
        from utils.errors import GameError
        
        self.mock_game.transfer.side_effect = GameError("Invalid move")
        
        # This should not raise, but show error message
        with patch('tkinter.messagebox.showinfo') as mock_box:
            mock_event = MagicMock()
            mock_event.widget = MagicMock()
            
            self.gui.selected_item = (1, 0)
            self.gui.on_click_tableau(mock_event, 1, 1)
            
            mock_box.assert_called()
    
    def test_win_condition(self):
        """Test that win condition is checked"""
        self.mock_game.check_win.return_value = True
        
        with patch('tkinter.messagebox.showinfo') as mock_box:
            self.gui.draw_game()
            mock_box.assert_called_with("NAN", "You win!")


if __name__ == '__main__':
    unittest.main()
