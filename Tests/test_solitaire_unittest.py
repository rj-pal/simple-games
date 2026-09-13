"""
test_solitaire_unittest.py
Comprehensive unit tests for the Solitaire game class using unittest.
Tests include edge cases, empty pile scenarios, invalid moves, and game logic.
No external dependencies required beyond Python standard library and game related modules.
"""

import unittest
from games.solitaire import Solitare
from core.deck import *
from utils.errors import *
from collections import deque

# ============================================================================
# UNIT TESTS
# ============================================================================

class TestSolitaireInitialization(unittest.TestCase):
    """Tests for game initialization."""
    
    def test_default_initialization(self):
        """Test that game initializes with default values."""
        game = Solitare()
        self.assertEqual(game.size, 7)
        self.assertEqual(game.klondike_value, 3)
        self.assertEqual(len(game.tableau), 7)
        self.assertEqual(len(game.foundation_piles), 4)
        
    def test_custom_size_initialization(self):
        """Test initialization with custom size."""
        game = Solitare(size=8, klondike_value=1)
        self.assertEqual(game.size, 8)
        self.assertEqual(game.klondike_value, 1)
        self.assertEqual(len(game.tableau), 8)
    
    def test_initial_tableau_distribution(self):
        """Test that tableau is created with correct card counts."""
        game = Solitare()
        for i, stack in enumerate(game.tableau):
            self.assertEqual(stack.size, i + 1)
    
    def test_foundation_piles_initialized_empty(self):
        """Test that all foundation piles start empty."""
        game = Solitare()
        for suit in ['S', 'H', 'D', 'C']:
            self.assertTrue(game.foundation_piles[suit].is_empty())


class TestSolitaireProperties(unittest.TestCase):
    """Tests for property setters and getters."""
    
    def test_size_property_valid_values(self):
        """Test size property accepts valid values."""
        game = Solitare()
        for valid_size in {6, 7, 8, 9, 10}:
            game.size = valid_size
            self.assertEqual(game.size, valid_size)
    
    def test_size_property_invalid_values(self):
        """Test size property rejects invalid values."""
        game = Solitare()
        with self.assertRaises(ValueError):
            game.size = 5
        with self.assertRaises(ValueError):
            game.size = 11
    
    def test_klondike_value_property_valid_values(self):
        """Test klondike_value property accepts valid values."""
        game = Solitare()
        game.klondike_value = 1
        self.assertEqual(game.klondike_value, 1)
        game.klondike_value = 3
        self.assertEqual(game.klondike_value, 3)
    
    def test_klondike_value_property_invalid_values(self):
        """Test klondike_value property rejects invalid values."""
        game = Solitare()
        with self.assertRaises(ValueError):
            game.klondike_value = 2
        with self.assertRaises(ValueError):
            game.klondike_value = 0


class TestCheckMove(unittest.TestCase):
    """Tests for tableau move validation."""
    
    def test_valid_move_king_to_empty(self):
        """Test that a King can be moved to an empty stack."""
        game = Solitare()
        king_of_spades = StandardCard('S', 13)
        empty_card = StandardCard('B', 0)
        self.assertTrue(game.check_move(king_of_spades, empty_card))
    
    def test_invalid_move_non_king_to_empty(self):
        """Test that non-Kings cannot be moved to empty stack."""
        game = Solitare()
        queen = StandardCard('S', 12)
        empty_card = StandardCard('B', 0)
        self.assertFalse(game.check_move(queen, empty_card))
    
    def test_valid_move_alternating_colors(self):
        """Test valid move with alternating colors and descending value."""
        game = Solitare()
        queen_red = StandardCard('H', 12)  # Heart (red)
        king_black = StandardCard('S', 13)  # Spade (black) - King is 13
        self.assertTrue(game.check_move(queen_red, king_black))
    
    def test_invalid_move_same_color(self):
        """Test that same color moves are invalid."""
        game = Solitare()
        queen_spade = StandardCard('S', 12)
        jack_spade = StandardCard('S', 11)
        self.assertFalse(game.check_move(queen_spade, jack_spade))
    
    def test_invalid_move_wrong_value_sequence(self):
        """Test that non-sequential values are invalid."""
        game = Solitare()
        queen_red = StandardCard('H', 12)
        ten_black = StandardCard('S', 10)
        self.assertFalse(game.check_move(queen_red, ten_black))


class TestCheckFoundationMove(unittest.TestCase):
    """Tests for foundation move validation."""
    
    def test_valid_first_card_ace(self):
        """Test that an Ace can start a foundation pile."""
        game = Solitare()
        ace = StandardCard('S', 1)
        self.assertTrue(game.check_foundation_move(ace))
    
    def test_invalid_first_card_non_ace(self):
        """Test that non-Aces cannot start a foundation pile."""
        game = Solitare()
        two = StandardCard('S', 2)
        self.assertFalse(game.check_foundation_move(two))
    
    def test_valid_sequential_foundation_move(self):
        """Test valid sequential moves on foundation pile."""
        game = Solitare()
        ace = StandardCard('S', 1)
        game.foundation_piles['S'].add_to(ace)
        
        two = StandardCard('S', 2)
        self.assertTrue(game.check_foundation_move(two))
    
    def test_invalid_wrong_suit_foundation_move(self):
        """Test that wrong suit cards cannot be placed on foundation."""
        game = Solitare()
        ace_spade = StandardCard('S', 1)
        game.foundation_piles['S'].add_to(ace_spade)
        
        two_heart = StandardCard('H', 2)
        self.assertFalse(game.check_foundation_move(two_heart))


class TestDrawAndWasteLogic(unittest.TestCase):
    """Tests for draw and waste pile operations."""
    
    def test_draw_with_klondike_value_1(self):
        """Test drawing 1 card at a time."""
        game = Solitare(klondike_value=1)
        initial_waste_size = game.waste_pile.size
        game.draw()
        self.assertEqual(game.waste_pile.size, initial_waste_size + 1)
    
    def test_draw_with_klondike_value_3(self):
        """Test drawing 3 cards at a time."""
        game = Solitare(klondike_value=3)
        initial_waste_size = game.waste_pile.size
        game.draw()
        self.assertEqual(game.waste_pile.size, initial_waste_size + 3)
    
    def test_draw_from_empty_pile_raises_error(self):
        """Test that drawing from empty pile raises EmptyPileError."""
        game = Solitare()
        while not game.draw_pile.is_empty():
            game.draw_pile.remove_from()
        
        with self.assertRaises(EmptyPileError):
            game.draw()
    
    def test_draw_cards_are_flipped(self):
        """Test that drawn cards are flipped to visible."""
        game = Solitare()
        game.draw()
        if not game.waste_pile.is_empty():
            top_card = game.waste_pile.get_card_in_play()
            self.assertTrue(top_card.visible)
    
    def test_reset_pile_with_full_draw_pile_fails(self):
        """Test that reset_pile fails if draw pile is not empty."""
        game = Solitare()
        with self.assertRaises(InvalidMoveError):
            game.reset_pile()
    
    def test_reset_pile_success(self):
        """Test successful pile reset."""
        game = Solitare()
        while not game.draw_pile.is_empty():
            game.draw_pile.remove_from()
        
        game.waste_pile.add_to(StandardCard('S', 5))
        game.waste_pile.add_to(StandardCard('H', 10))
        
        initial_waste_size = game.waste_pile.size
        self.assertTrue(game.reset_pile())
        self.assertTrue(game.waste_pile.is_empty())
        self.assertEqual(game.draw_pile.size, initial_waste_size)


class TestBuildOperation(unittest.TestCase):
    """Tests for building cards from waste to tableau."""
    
    def test_build_from_empty_waste_fails(self):
        """Test that building from empty waste pile fails."""
        game = Solitare()
        with self.assertRaises(EmptyPileError):
            game.build(0)
    
    def test_build_invalid_stack_number(self):
        """Test that invalid stack numbers are rejected."""
        game = Solitare()
        game.waste_pile.add_to(StandardCard('S', 5))
        
        with self.assertRaises(InvalidStackError):
            game.build(-1)
        with self.assertRaises(InvalidStackError):
            game.build(game.size)
    
    def test_build_valid_move(self):
        """Test valid build operation."""
        game = Solitare()
        king = StandardCard('S', 13)
        king.flip_card()
        game.tableau[0].add_to(king)
        
        queen_red = StandardCard('H', 12)
        queen_red.flip_card()
        game.waste_pile.add_to(queen_red)
        
        self.assertTrue(game.build(0))
        self.assertTrue(game.waste_pile.is_empty())
        self.assertEqual(game.tableau[0].get_card_in_play(), queen_red)
    
    def test_build_invalid_move(self):
        """Test that invalid build moves are rejected."""
        game = Solitare()
        jack = StandardCard('S', 11)
        jack.flip_card()
        game.tableau[0].add_to(jack)
        
        queen = StandardCard('S', 12)
        queen.flip_card()
        game.waste_pile.add_to(queen)
        
        with self.assertRaises(InvalidMoveError):
            game.build(0)


class TestTransferOperation(unittest.TestCase):
    """Tests for transferring cards between tableau stacks."""
    
    def test_transfer_from_empty_stack_fails(self):
        """Test that transferring from empty stack fails."""
        game = Solitare()
        # Clear the source stack to make it empty
        while not game.tableau[0].is_empty():
            game.tableau[0].remove_from()
        # Now try to transfer from empty stack
        with self.assertRaises(EmptyPileError):
            game.transfer(0, 1, 1)
    
    def test_transfer_invalid_source_stack(self):
        """Test that invalid source stack raises error."""
        game = Solitare()
        with self.assertRaises(InvalidStackError):
            game.transfer(-1, 1, 1)
        with self.assertRaises(InvalidStackError):
            game.transfer(game.size, 1, 1)
    
    def test_transfer_invalid_destination_stack(self):
        """Test that invalid destination stack raises error."""
        game = Solitare()
        game.tableau[0].add_to(StandardCard('S', 13))
        with self.assertRaises(InvalidStackError):
            game.transfer(0, game.size, 1)
    
    def test_transfer_zero_cards_fails(self):
        """Test that transferring zero or negative cards fails."""
        game = Solitare()
        game.tableau[0].add_to(StandardCard('S', 13))
        with self.assertRaises(InvalidMoveError):
            game.transfer(0, 1, 0)
        with self.assertRaises(InvalidMoveError):
            game.transfer(0, 1, -1)
    
    def test_transfer_more_cards_than_exist_fails(self):
        """Test that transferring more cards than in stack fails."""
        game = Solitare()
        game.tableau[0].add_to(StandardCard('S', 13))
        with self.assertRaises(InvalidMoveError):
            game.transfer(0, 1, 5)
    
    def test_transfer_face_down_card_fails(self):
        """Test that transferring face-down cards fails."""
        game = Solitare()
        face_down = StandardCard('S', 13)
        face_down.visible = False
        game.tableau[0].add_to(face_down)
        
        with self.assertRaises(InvalidMoveError):
            game.transfer(0, 1, 1)
    
    def test_transfer_valid_single_card(self):
        """Test valid single card transfer."""
        game = Solitare()
        # Clear destination tableau
        while not game.tableau[1].is_empty():
            game.tableau[1].remove_from()
        
        # Set up source with Queen visible
        while not game.tableau[0].is_empty():
            game.tableau[0].remove_from()
        queen_red = StandardCard('H', 12)
        queen_red.flip_card()
        game.tableau[0].add_to(queen_red)
        
        # Set up destination with King visible
        king_black = StandardCard('S', 13)
        king_black.flip_card()
        game.tableau[1].add_to(king_black)
        
        # Transfer Queen (12) under King (13) should work
        self.assertTrue(game.transfer(0, 1, 1))


class TestFoundationMoves(unittest.TestCase):
    """Tests for moving cards to/from foundation piles."""
    
    def test_move_to_foundation_from_empty_pile(self):
        """Test that moving from empty pile fails."""
        game = Solitare()
        with self.assertRaises(EmptyPileError):
            game.move_to_foundation("waste_pile")
    
    def test_move_to_foundation_invalid_source(self):
        """Test that invalid source raises error."""
        game = Solitare()
        with self.assertRaises(ValueError):
            game.move_to_foundation("invalid_source")
    
    def test_move_ace_to_foundation_from_waste(self):
        """Test moving Ace from waste to foundation."""
        game = Solitare()
        ace_spade = StandardCard('S', 1)
        ace_spade.flip_card()
        game.waste_pile.add_to(ace_spade)
        
        self.assertTrue(game.move_to_foundation("waste_pile"))
        self.assertEqual(game.foundation_piles['S'].get_card_in_play(), ace_spade)
        self.assertTrue(game.waste_pile.is_empty())
    
    def test_move_non_ace_to_empty_foundation(self):
        """Test that non-Ace cannot start foundation pile."""
        game = Solitare()
        two_spade = StandardCard('S', 2)
        two_spade.flip_card()
        game.waste_pile.add_to(two_spade)
        
        with self.assertRaises(InvalidMoveError):
            game.move_to_foundation("waste_pile")
    
    def test_move_to_foundation_from_tableau(self):
        """Test moving card from tableau to foundation."""
        game = Solitare()
        ace_heart = StandardCard('H', 1)
        ace_heart.flip_card()
        game.tableau[0].add_to(ace_heart)
        
        self.assertTrue(game.move_to_foundation("tableau", stack_number=0))
        self.assertEqual(game.foundation_piles['H'].get_card_in_play(), ace_heart)


class TestWinCondition(unittest.TestCase):
    """Tests for win condition checking."""
    
    def test_check_win_new_game(self):
        """Test that new game is not won."""
        game = Solitare()
        self.assertFalse(game.check_win())
    
    def test_check_win_partial_foundation(self):
        """Test that game with partial foundation is not won."""
        game = Solitare()
        for i in range(1, 14):
            game.foundation_piles['S'].add_to(StandardCard('S', i))
        
        self.assertFalse(game.check_win())
    
    def test_check_win_all_foundation_filled(self):
        """Test win condition when all foundations filled."""
        game = Solitare()
        for suit in ['S', 'H', 'D', 'C']:
            for value in range(1, 14):
                game.foundation_piles[suit].add_to(StandardCard(suit, value))
        
        self.assertTrue(game.check_win())


class TestCustomTableau(unittest.TestCase):
    """Tests using custom-built tableau scenarios."""
    
    def setUp(self):
        """Setup a fresh game for each test."""
        self.game = Solitare()
    
    def test_custom_tableau_king_to_empty_sequence(self):
        """Test King placement and building sequence."""
        tableau = self.game.tableau
        
        # Set up source stack with King
        while not tableau[0].is_empty():
            tableau[0].remove_from()
        king_spade = StandardCard('S', 13)
        king_spade.flip_card()
        tableau[0].add_to(king_spade)
        
        # Set up destination stack - should be empty for King to go there
        while not tableau[1].is_empty():
            tableau[1].remove_from()
        
        # Transfer King to empty tableau should work
        self.assertTrue(self.game.transfer(0, 1, 1))
        self.assertEqual(tableau[1].get_card_in_play().value, 13)
    
    def test_custom_waste_pile_sequence(self):
        """Test custom waste pile operations."""
        waste = self.game.waste_pile
        
        cards = [StandardCard('S', i) for i in range(1, 5)]
        for card in cards:
            card.flip_card()
            waste.add_to(card)
        
        self.assertEqual(waste.size, 4)
        
        last_card = waste.remove_from()
        self.assertEqual(last_card.value.value, 4)
        self.assertEqual(waste.size, 3)
    
    def test_empty_pile_operations(self):
        """Test operations on empty piles."""
        empty_stack = CardStack()
        
        self.assertTrue(empty_stack.is_empty())
        self.assertEqual(empty_stack.size, 0)
        
        with self.assertRaises(EmptyPileError):
            empty_stack.remove_from()
        
        self.assertEqual(empty_stack.get_card_in_play().value, 0)


class TestComplexGameScenarios(unittest.TestCase):
    """Tests for complex game scenarios."""
    
    def setUp(self):
        self.game = Solitare()
    
    def test_multiple_draws_depletes_draw_pile(self):
        """Test that multiple draws eventually empty the draw pile."""
        draw_count = 0
        
        while not self.game.draw_pile.is_empty():
            try:
                self.game.draw()
                draw_count += 1
            except EmptyPileError:
                break
        
        self.assertTrue(self.game.draw_pile.is_empty())
        self.assertGreater(draw_count, 0)
    
    def test_waste_pile_accumulation(self):
        """Test that waste pile accumulates cards correctly."""
        initial_waste = self.game.waste_pile.size
        self.game.draw()
        self.assertGreater(self.game.waste_pile.size, initial_waste)
    
    def test_tableau_card_visibility(self):
        """Test that only top card in tableau is visible initially."""
        for stack in self.game.tableau:
            visible_count = sum(0 if card == "🎴" else 1 for card in stack.to_list())
            self.assertEqual(visible_count, 1)
    
    def test_move_card_method(self):
        """Test the move_card method directly."""
        source = CardStack()
        dest = CardStack()
        
        card = StandardCard('S', 5)
        source.add_to(card)
        
        self.game.move_card(source, dest, flip_card=False)
        
        self.assertTrue(source.is_empty())
        self.assertEqual(dest.get_card_in_play(), card)


# ============================================================================
# TEST RUNNER
# ============================================================================

if __name__ == "__main__":
    # Run tests with verbose output
    unittest.main(verbosity=2)
