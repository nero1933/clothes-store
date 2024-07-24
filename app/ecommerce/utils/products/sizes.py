# "size_categories" has to be a list of categories.
size_categories = ['shoes', 'clothes']

# range of shoes sizes.
shoes_sizes_start = 35
shoes_sizes_stop = 50
shoes_sizes_step = 1 # can be 0.5.

# PRODUCT SIZE CHOICES.
shoes_sizes = [(str(i), str(i)) for i in range(shoes_sizes_start, shoes_sizes_stop, shoes_sizes_step)]
clothes_sizes = [
    ('XS', 'Extra Small'),
    ('S', 'Small'),
    ('M', 'Medium'),
    ('L', 'Large'),
    ('XL', 'Extra Large'),
]