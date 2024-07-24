# Product size starts!

# Range of shoes sizes.
shoes_sizes_start = 35
shoes_sizes_stop = 50
shoes_sizes_step = 1 # can be 0.5.

# Size names for each of categories.
shoes_sizes = [(str(i), str(i)) for i in range(shoes_sizes_start, shoes_sizes_stop, shoes_sizes_step)]
clothes_sizes = [
    ('XS', 'Extra Small'),
    ('S', 'Small'),
    ('M', 'Medium'),
    ('L', 'Large'),
    ('XL', 'Extra Large'),
]
bag_size = [
    ('2 L', '2 l'),
    ('6 L', '6 l'),
    ('12 L', '12 l'),
    ('16 L', '16 l'),
    ('20 L', '20 l'),
    ('26 L', '26 l'),
    ('31 L', '31 l'),
]

# PRODUCT_SIZE_CHOICES.
PRODUCT_SIZE_CHOICES = shoes_sizes + clothes_sizes + bag_size

# Product size ends!

# ---------- #

# Sizes starts!

# Used in "create_sizes_command".
sizes = {
    'SHOES': shoes_sizes,
    'CLOTHES': clothes_sizes,
    'BAGS': bag_size,
}

# Sizes ends!

# ---------- #

# Size categories starts!

# "size_categories" has to be a list of categories.
size_categories = [category for category in sizes.keys()]

# SIZE_CATEGORY_CHOICES.
SIZE_CATEGORY_CHOICES = [(cat, cat.lower()) for cat in size_categories]

# Size categories ends!
