2025-02-27  Emil Viesná  <snowboard_refinery@proton.me>

	Release for Python 3.12

2024-08-03  Emil Viesná  <snowboard_refinery@proton.me>

	Performance optimization

	* src/pawpyrus/main.py: AlphaEncoder class removed, script structure is now
	plain; most parameters are pre-calculated, which improves performance.
	* pyproject.toml: New repo address added.
	* CHANGELOG.md: Created.

2024-03-24  Emil Viesná  <snowboard_refinery@proton.me>

	Fixed cv2.aruco bug (namespace changes); tested with Python 3.11.2
