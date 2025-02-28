# Card Game (Eleusis) Rules

The Eleusis module provides specialized rules and objects for validating card game sequences, particularly for the game of Eleusis. It supports various aspects of card game rules including:
- Card properties (suit, rank, color)
- Pattern matching
- Sequence relationships
- Complex rule combinations
- Game state tracking

## Basic Usage

```python
from seqrule import AbstractObject
from seqrule.rulesets.eleusis import (
    create_suit_rule,
    create_rank_rule,
    create_alternating_rule
)

# Create a card sequence
sequence = [
    AbstractObject(suit="hearts", rank=7, color="red"),
    AbstractObject(suit="spades", rank=8, color="black"),
    AbstractObject(suit="diamonds", rank=9, color="red"),
]

# Check suit pattern
suit_rule = create_suit_rule(
    pattern=["hearts", "spades", "diamonds"]
)
is_valid = suit_rule(sequence)  # True

# Check alternating colors
alternating = create_alternating_rule("color")
alternates = alternating(sequence)  # True
```

## Card Rules

### Suit Rules

```python
def create_suit_rule(pattern=None, forbidden=None):
    """
    Create a rule checking suit patterns.
    
    Args:
        pattern (list[str], optional): Required suit pattern
        forbidden (list[str], optional): Forbidden suits
        
    Returns:
        Rule: A rule checking suit requirements
        
    Example:
        >>> red_suits = create_suit_rule(
        ...     pattern=["hearts", "diamonds"]
        ... )
        >>> red_suits(sequence)  # True if only red suits
    """
```

### Rank Rules

```python
def create_rank_rule(
    trend=None,
    modulo=None,
    difference=None
):
    """
    Create a rule checking rank relationships.
    
    Args:
        trend (str, optional): Trend type ("ascending", "descending")
        modulo (int, optional): Modulo relationship
        difference (int, optional): Required difference
        
    Returns:
        Rule: A rule checking rank relationships
        
    Example:
        >>> ascending = create_rank_rule(trend="ascending")
        >>> ascending(sequence)  # True if ranks increase
    """
```

### Property Relationships

```python
def create_relationship_rule(
    property_name,
    relationship_type
):
    """
    Create a rule checking property relationships.
    
    Args:
        property_name (str): Name of the property
        relationship_type (str): Type of relationship
        
    Returns:
        Rule: A rule checking relationships
        
    Example:
        >>> alternating = create_relationship_rule(
        ...     "color", 
        ...     "alternating"
        ... )
        >>> alternating(sequence)  # True if colors alternate
    """
```

## Advanced Features

### Pattern Matching

```python
def create_pattern_rule(
    pattern_type,
    length=3,
    cyclic=True
):
    """
    Create a rule checking for patterns.
    
    Args:
        pattern_type (str): Type of pattern to match
        length (int): Length of pattern
        cyclic (bool): Whether pattern repeats
        
    Returns:
        Rule: A rule checking for patterns
        
    Example:
        >>> pattern = create_pattern_rule("suit_color")
        >>> pattern(sequence)  # True if pattern matches
    """
```

### State Tracking

```python
def create_state_rule(
    property_name,
    state_function
):
    """
    Create a rule tracking game state.
    
    Args:
        property_name (str): Property to track
        state_function (callable): State update function
        
    Returns:
        Rule: A rule tracking state
        
    Example:
        >>> def count_hearts(state, card):
        ...     return state + (1 if card.suit == "hearts" else 0)
        >>> hearts = create_state_rule("suit", count_hearts)
        >>> hearts(sequence)  # True if state valid
    """
```

### Complex Rules

Combine multiple rules for comprehensive validation:

```python
from seqrule import And, Or, Not

# Create a complex card rule
card_rule = And(
    create_suit_rule(pattern=["hearts", "spades"]),
    create_rank_rule(trend="ascending"),
    Not(create_suit_rule(forbidden=["clubs"]))
)

# Create a flexible pattern rule
pattern_rule = Or(
    create_pattern_rule("suit_color", length=2),
    create_pattern_rule("rank_parity", length=3)
)
```

## Best Practices

### 1. Card Validation

Always validate card properties:
```python
def validate_card(card):
    """Check if card has required properties."""
    required = {"suit", "rank", "color"}
    return all(
        hasattr(card, prop)
        for prop in required
    )
```

### 2. Property Normalization

Use consistent property formats:
```python
def normalize_card(card):
    """Normalize card properties."""
    if hasattr(card, "suit"):
        card.suit = card.suit.lower()
    if hasattr(card, "color"):
        card.color = card.color.lower()
    if hasattr(card, "rank"):
        if isinstance(card.rank, str):
            rank_map = {
                "A": 1, "J": 11,
                "Q": 12, "K": 13
            }
            card.rank = rank_map.get(
                card.rank.upper(),
                int(card.rank)
            )
    return card
```

### 3. Pattern Handling

Handle pattern matching efficiently:
```python
def match_pattern(sequence, pattern):
    """Match a sequence against a pattern."""
    if len(sequence) < len(pattern):
        return False
        
    for i in range(len(sequence) - len(pattern) + 1):
        window = sequence[i:i + len(pattern)]
        if all(
            getattr(card, "suit") == suit
            for card, suit in zip(window, pattern)
        ):
            return True
            
    return False
```

### 4. Error Handling

Handle missing or invalid properties gracefully:
```python
def get_card_value(card):
    """Get card value safely."""
    if not hasattr(card, "rank"):
        return None
    try:
        return int(card.rank)
    except (ValueError, TypeError):
        return None
```

## Performance Tips

1. Cache computed properties:
```python
class CardSequence:
    def __init__(self, sequence):
        self._sequence = sequence
        self._suit_counts = None
        self._rank_sum = None
        
    @property
    def suit_counts(self):
        if self._suit_counts is None:
            self._suit_counts = {}
            for card in self._sequence:
                if hasattr(card, "suit"):
                    suit = card.suit
                    self._suit_counts[suit] = \
                        self._suit_counts.get(suit, 0) + 1
        return self._suit_counts
        
    @property
    def rank_sum(self):
        if self._rank_sum is None:
            self._rank_sum = sum(
                card.rank for card in self._sequence
                if hasattr(card, "rank")
            )
        return self._rank_sum
```

2. Use efficient lookups:
```python
def find_cards(sequence, suit):
    """Find cards efficiently."""
    return [
        card for card in sequence
        if hasattr(card, "suit") and card.suit == suit
    ]
```

3. Implement early returns:
```python
def check_sequence(sequence, pattern):
    """Check sequence with early returns."""
    if not sequence:
        return False
        
    if len(sequence) < len(pattern):
        return False
        
    for card, expected in zip(sequence, pattern):
        if not hasattr(card, "suit"):
            return False
        if card.suit != expected:
            return False
            
    return True
```

## Card Constants

```python
# Card properties
SUITS = {
    "hearts": {"color": "red", "rank": "h"},
    "diamonds": {"color": "red", "rank": "d"},
    "clubs": {"color": "black", "rank": "c"},
    "spades": {"color": "black", "rank": "s"}
}

RANKS = {
    "A": 1,
    "2": 2, "3": 3, "4": 4, "5": 5,
    "6": 6, "7": 7, "8": 8, "9": 9,
    "10": 10, "J": 11, "Q": 12, "K": 13
}

# Pattern types
PATTERNS = {
    "suit_color": lambda card: (card.suit, card.color),
    "rank_parity": lambda card: card.rank % 2,
    "suit_rank": lambda card: (card.suit, card.rank),
    "color_rank": lambda card: (card.color, card.rank)
}

# Relationship types
RELATIONSHIPS = {
    "alternating": lambda x, y: x != y,
    "same": lambda x, y: x == y,
    "increasing": lambda x, y: y > x,
    "decreasing": lambda x, y: y < x
}
``` 