# ==========================
# Variables
# ==========================
NAME = amazing.py
PYTHON = python3
TEXT = config.txt

# ==========================
# Default rule
# ==========================
all: run

# ==========================
# Run program comme dans C tamzany
# ==========================
run:
	$(PYTHON) $(NAME) $(TEXT)

# ==========================
# Clean (cache python) mamafa cache de python __pychache__ voaforona apres execution programme
# ==========================
clean:
	rm -rf __pycache__
	find . -type d -name "__pycache__" -exec rm -rf {} +

# ==========================
# Full clean
# ==========================
fclean: clean

# ==========================
# Re-run clean build otrn tam C ihany fa version python
# ==========================
re: fclean all

# ==========================
# Helping be tss otrzany
# ==========================
help:
	@echo "make run   -> lancer le programme"
	@echo "make clean -> supprimer cache python"
	@echo "make re    -> clean + run"