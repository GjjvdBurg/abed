abed: Automated BEnchmark Distribution
======================================

Usage:

1. Create a skeleton for your project

	abed skeleton

2. Edit configuration, add datasets and executables, and git commit these
3. Create remote directory structure (this will also create task file from 
   config)

	abed setup

4. Push to server

	abed push

5. When tasks are done, collect results

	abed pull

6. Alternatively, automate push/pull using

	abed auto

7. Create summary files using the specified metrics using

	abed parse_results

