"""
Classic Eleusis card game rules.

This module implements both classic and creative rules for the Eleusis card game,
showcasing a wide range of pattern matching capabilities:

Classic Rules:
- Red/black alternation
- Suit cycles
- Fixed patterns
- Odd/even numbers
- Range-based rules
- Increment patterns

Creative Rules:
- Mathematical patterns
- Multi-card relationships
- Historical patterns
- Card properties combinations
- Complex sequences
- Meta-rules
"""

import math
from typing import Dict, List, Sequence

from ..core import AbstractObject
from ..dsl import DSLRule


class Card(AbstractObject):
    """A playing card with color, suit, and number properties."""

    def __init__(self, color: str, suit: str, number: int):
        """
        Initialize a card.

        Args:
            color: The card color ("red" or "black")
            suit: The card suit ("heart", "diamond", "spade", or "club")
            number: The card number (1-13, where Ace=1, Jack=11, Queen=12, King=13)
        """
        super().__init__(color=color, suit=suit, number=number)

    def __repr__(self) -> str:
        return (
            f"Card(color={self.properties['color']}, "
            f"suit={self.properties['suit']}, "
            f"number={self.properties['number']})"
        )


def is_odd(n: int) -> bool:
    """Return True if n is odd."""
    return n % 2 == 1


def is_even(n: int) -> bool:
    """Return True if n is even."""
    return n % 2 == 0


def alternation_rule(seq: Sequence[AbstractObject]) -> bool:
    """If the last card was red, play a black card. If black, play red."""
    if len(seq) < 2:
        return True  # no prior card or only starter exists
    last = seq[-2]  # last accepted card
    candidate = seq[-1]  # newly played card
    if last["color"] == "red":
        return candidate["color"] == "black"
    elif last["color"] == "black":
        return candidate["color"] == "red"
    return True


# The suit cycle: spade->heart->diamond->club->spade
SUIT_CYCLE = {"spade": "heart", "heart": "diamond", "diamond": "club", "club": "spade"}


def suit_cycle_rule(seq: Sequence[AbstractObject]) -> bool:
    """Follow the suit cycle: spade->heart->diamond->club->spade."""
    if len(seq) < 2:
        return True
    last = seq[-2]
    candidate = seq[-1]
    return SUIT_CYCLE[last["suit"]] == candidate["suit"]


def fixed_pattern_rule(seq: Sequence[AbstractObject]) -> bool:
    """Groups of 3 cards alternate between red and black."""
    if len(seq) < 1:
        return True
    group_size = 3
    # Get the color of the first card in the sequence to determine pattern
    first_color = seq[0]["color"]
    # Calculate which group the current card is in
    group_num = (len(seq) - 1) // group_size
    # Expected color alternates based on first card's color
    expected_color = (
        first_color
        if group_num % 2 == 0
        else ("black" if first_color == "red" else "red")
    )
    return seq[-1]["color"] == expected_color


def odd_even_rule(seq: Sequence[AbstractObject]) -> bool:
    """If last number was odd, next must be even; if even, next must be odd."""
    if len(seq) < 2:
        return True
    last = seq[-2]
    candidate = seq[-1]
    if is_odd(last["number"]):
        return is_even(candidate["number"])
    elif is_even(last["number"]):
        return is_odd(candidate["number"])
    return True


def range_rule(seq: Sequence[AbstractObject]) -> bool:
    """If last number was 1-7, next must be 8-13; if 8-13, next must be 1-7."""
    if len(seq) < 2:
        return True
    last = seq[-2]
    candidate = seq[-1]
    if 1 <= last["number"] <= 7:
        return 8 <= candidate["number"] <= 13
    elif 8 <= last["number"] <= 13:
        return 1 <= candidate["number"] <= 7
    return True


def increment_rule(seq: Sequence[AbstractObject]) -> bool:
    """Next card's number must be 1-3 higher (modulo 13) than the last card."""
    if len(seq) < 2:
        return True
    last = seq[-2]
    candidate = seq[-1]
    diff = (candidate["number"] - last["number"]) % 13
    return 1 <= diff <= 3


def hard_odd_even_color_rule(seq: Sequence[AbstractObject]) -> bool:
    """If current number is odd, it must be red; if even, it must be black."""
    if len(seq) < 1:
        return True
    candidate = seq[-1]
    if is_odd(candidate["number"]):
        return candidate["color"] == "red"
    elif is_even(candidate["number"]):
        return candidate["color"] == "black"
    return True


def matching_rule(seq: Sequence[AbstractObject]) -> bool:
    """Next card must match previous card's suit or number."""
    if len(seq) < 2:
        return True
    last = seq[-2]
    candidate = seq[-1]
    return candidate["suit"] == last["suit"] or candidate["number"] == last["number"]


def comparative_rule(seq: Sequence[AbstractObject]) -> bool:
    """If current card is black, its number must be <= previous; if red, its number must be >= previous."""
    if len(seq) < 2:
        return True
    for i in range(1, len(seq)):
        current = seq[i]
        prev = seq[i - 1]
        # For black cards, current number must be less than or equal to previous
        if current["color"] == "black":
            if current["number"] > prev["number"]:
                return False
        # For red cards, current number must be greater than or equal to previous
        elif current["color"] == "red":
            if current["number"] < prev["number"]:
                return False
    return True


def fibonacci_rule(seq: Sequence[AbstractObject]) -> bool:
    """Numbers must follow Fibonacci sequence (mod 13)."""
    if len(seq) < 3:
        return True
    last_three = seq[-3:]
    nums = [n["number"] for n in last_three]
    return (nums[2] % 13) == ((nums[0] + nums[1]) % 13)


def prime_sum_rule(seq: Sequence[AbstractObject]) -> bool:
    """Sum of last three numbers must be prime."""

    def is_prime(n: int) -> bool:
        if n < 2:
            return False
        return all(n % i != 0 for i in range(2, int(math.sqrt(n)) + 1))

    if len(seq) < 3:
        return True
    last_three = seq[-3:]
    total = sum(card["number"] for card in last_three)
    return is_prime(total)


def royal_sequence_rule(seq: Sequence[AbstractObject]) -> bool:
    """
    Face cards must appear in order: Jack -> Queen -> King,
    with any number of non-face cards between them.
    """
    if len(seq) < 2:
        return True

    # Track the last face card seen
    last_face = None
    for card in seq:
        num = card["number"]
        if num in {11, 12, 13}:  # Face cards
            if last_face is None and num != 11:  # Must start with Jack
                return False
            if last_face == 11 and num != 12:  # Jack must be followed by Queen
                return False
            if last_face == 12 and num != 13:  # Queen must be followed by King
                return False
            last_face = num
    return True


def create_suit_value_rule(suit_values: Dict[str, int]) -> DSLRule:
    """
    Creates a rule where each suit has a point value, and consecutive
    cards must increase the total score.

    Example:
        hearts_high = create_suit_value_rule({
            "heart": 4, "diamond": 3, "club": 2, "spade": 1
        })
    """

    def check_suit_values(seq: Sequence[AbstractObject]) -> bool:
        if len(seq) < 2:
            return True

        def card_value(card: AbstractObject) -> int:
            return suit_values[card["suit"]] * card["number"]

        last_value = card_value(seq[-2])
        current_value = card_value(seq[-1])
        return current_value > last_value

    return DSLRule(check_suit_values, "Card values must increase")


def create_historical_rule(window: int = 3) -> DSLRule:
    """
    Creates a rule requiring new cards to match a property
    (color, suit, or number) from the historical window.

    Example:
        historical = create_historical_rule(3)  # Must match last 3 cards
    """

    def check_historical(seq: Sequence[AbstractObject]) -> bool:
        if len(seq) <= window:
            return True

        current = seq[-1]
        history = seq[-window - 1 : -1]

        # Must match at least one property from history
        return any(
            current["color"] == card["color"]
            or current["suit"] == card["suit"]
            or current["number"] == card["number"]
            for card in history
        )

    return DSLRule(check_historical, f"Must match a property from last {window} cards")


def create_meta_rule(rules: List[DSLRule], required_count: int) -> DSLRule:
    """
    Creates a meta-rule requiring a certain number of other rules to be satisfied.

    Example:
        two_of_three = create_meta_rule([rule1, rule2, rule3], 2)
    """

    def check_meta(seq: Sequence[AbstractObject]) -> bool:
        satisfied = sum(1 for rule in rules if rule(seq))
        return satisfied >= required_count

    return DSLRule(
        check_meta, f"Must satisfy at least {required_count} of {len(rules)} rules"
    )


def create_symmetry_rule(length: int = 3) -> DSLRule:
    """
    Creates a rule requiring symmetry in card properties over a window.

    Example:
        symmetry = create_symmetry_rule(3)  # A-B-A pattern
    """

    def check_symmetry(seq: Sequence[AbstractObject]) -> bool:
        if len(seq) < length:
            return True

        window = seq[-length:]
        for i in range(length // 2):
            left = window[i]
            right = window[-(i + 1)]
            if not (
                left["color"] == right["color"]
                or left["suit"] == right["suit"]
                or left["number"] == right["number"]
            ):
                return False
        return True

    return DSLRule(check_symmetry, f"Symmetric pattern over {length} cards")


def create_property_cycle_rule(*properties: str) -> DSLRule:
    """Create a rule that requires at least one consecutive pair of cards to match on each property in the cycle.

    Args:
        *properties: Variable number of property names to check for matches.

    Returns:
        A rule that returns True if at least one consecutive pair matches on each property in the cycle.
    """

    def property_cycle_rule(seq: List[Card]) -> bool:
        if len(seq) < 2:
            return True

        # Track which properties have been matched
        matched_properties = set()

        # Check each consecutive pair
        for i in range(len(seq) - 1):
            # Get current and next card
            curr_card = seq[i]
            next_card = seq[i + 1]

            # Check which properties match for this pair
            for prop in properties:
                if curr_card[prop] == next_card[prop]:
                    print(
                        f"Pair {i} matches on {prop}: {curr_card[prop]} == {next_card[prop]}"
                    )
                    matched_properties.add(prop)
                else:
                    print(
                        f"Pair {i} does not match on {prop}: {curr_card[prop]} != {next_card[prop]}"
                    )

        # Check if we found a match for each property
        return len(matched_properties) == len(properties)

    return DSLRule(
        property_cycle_rule,
        f"Each consecutive pair matches on cycling properties: {', '.join(properties)}",
    )


# Create DSL rules for each function
alternation_dsl = DSLRule(
    alternation_rule,
    "Alternation: if last card is red, next is black; if black, next is red",
)

suit_cycle_dsl = DSLRule(
    suit_cycle_rule, "Suit Cycle: follow spade->heart->diamond->club->spade"
)

fixed_pattern_dsl = DSLRule(
    fixed_pattern_rule, "Fixed Pattern: groups of 3 cards alternate red and black"
)

odd_even_dsl = DSLRule(
    odd_even_rule, "Odd/Even: if last number is odd, next is even; if even, next is odd"
)

range_dsl = DSLRule(
    range_rule, "Range Rule: if last number is 1-7, next is 8-13; else vice versa"
)

increment_dsl = DSLRule(
    increment_rule, "Increment: next card's number is 1-3 higher modulo 13"
)

hard_odd_even_color_dsl = DSLRule(
    hard_odd_even_color_rule,
    "Hard Odd/Even Color: if current number is odd, it must be red; if even, it must be black",
)

matching_dsl = DSLRule(
    matching_rule, "Matching: next card matches last card in suit or number"
)

comparative_dsl = DSLRule(
    comparative_rule,
    "Comparative: if current card is black, its number must be <= previous; if red, its number must be >= previous",
)

fibonacci_dsl = DSLRule(fibonacci_rule, "Numbers follow Fibonacci sequence modulo 13")

prime_sum_dsl = DSLRule(prime_sum_rule, "Sum of last three numbers is prime")

royal_sequence_dsl = DSLRule(royal_sequence_rule, "Face cards appear in order: J->Q->K")

# Create example rules
hearts_high = create_suit_value_rule({"heart": 4, "diamond": 3, "club": 2, "spade": 1})

historical_pattern = create_historical_rule(3)

symmetry_rule = create_symmetry_rule(3)

property_cycle = create_property_cycle_rule("color", "number")

# Complex rule combinations
mathematical_rules = create_meta_rule(
    [fibonacci_dsl, prime_sum_dsl, range_dsl], required_count=2
)

royal_rules = create_meta_rule(
    [royal_sequence_dsl, matching_dsl, comparative_dsl], required_count=2
)

pattern_rules = create_meta_rule(
    [symmetry_rule, property_cycle, historical_pattern], required_count=2
)

# Collection of all rules, organized by category
eleusis_rules: Dict[str, DSLRule] = {
    # Classic Rules
    "alternation": alternation_dsl,
    "suit_cycle": suit_cycle_dsl,
    "fixed_pattern": fixed_pattern_dsl,
    "odd_even": odd_even_dsl,
    "range": range_dsl,
    "increment": increment_dsl,
    "hard_odd_even_color": hard_odd_even_color_dsl,
    "matching": matching_dsl,
    "comparative": comparative_dsl,
    # Mathematical Rules
    "fibonacci": fibonacci_dsl,
    "prime_sum": prime_sum_dsl,
    # Card Relationship Rules
    "royal_sequence": royal_sequence_dsl,
    "hearts_high": hearts_high,
    "historical_pattern": historical_pattern,
    "symmetry": symmetry_rule,
    # Property Rules
    "property_cycle": property_cycle,
    # Meta Rules
    "mathematical_combo": mathematical_rules,
    "royal_combo": royal_rules,
    "pattern_combo": pattern_rules,
}

# Rule categories for easier access
classic_rules = {
    key: eleusis_rules[key]
    for key in [
        "alternation",
        "suit_cycle",
        "fixed_pattern",
        "odd_even",
        "range",
        "increment",
        "hard_odd_even_color",
        "matching",
        "comparative",
    ]
}

mathematical_rules = {key: eleusis_rules[key] for key in ["fibonacci", "prime_sum"]}

relationship_rules = {
    key: eleusis_rules[key]
    for key in ["royal_sequence", "hearts_high", "historical_pattern", "symmetry"]
}

property_rules = {key: eleusis_rules[key] for key in ["property_cycle"]}

meta_rules = {
    key: eleusis_rules[key]
    for key in ["mathematical_combo", "royal_combo", "pattern_combo"]
}

# Example rule combinations for different difficulty levels
beginner_rules = [
    eleusis_rules["alternation"],
    eleusis_rules["odd_even"],
    eleusis_rules["matching"],
]

intermediate_rules = [
    eleusis_rules["suit_cycle"],
    eleusis_rules["royal_sequence"],
    eleusis_rules["historical_pattern"],
]

advanced_rules = [
    eleusis_rules["fibonacci"],
    eleusis_rules["symmetry"],
    eleusis_rules["pattern_combo"],
]

# Create meta-rules for different difficulty levels
beginner_meta = create_meta_rule(beginner_rules, 2)
intermediate_meta = create_meta_rule(intermediate_rules, 2)
advanced_meta = create_meta_rule(advanced_rules, 2)

# Example sequences demonstrating creative rules
fibonacci_sequence = [
    Card(color="red", suit="heart", number=1),
    Card(color="black", suit="spade", number=1),
    Card(color="red", suit="diamond", number=2),
    Card(color="black", suit="club", number=3),
    Card(color="red", suit="heart", number=5),
]

royal_pattern = [
    Card(color="red", suit="heart", number=11),  # Jack
    Card(color="black", suit="spade", number=5),  # Non-face
    Card(color="red", suit="diamond", number=12),  # Queen
    Card(color="black", suit="club", number=7),  # Non-face
    Card(color="red", suit="heart", number=13),  # King
]

symmetric_pattern = [
    Card(color="red", suit="heart", number=7),
    Card(color="black", suit="spade", number=10),
    Card(color="red", suit="diamond", number=7),
]
