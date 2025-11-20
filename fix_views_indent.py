# fix_views_indent.py
import re, shutil, pathlib, datetime, sys

p = pathlib.Path("freelancer/views.py")
if not p.exists():
    print("ERROR: freelancer/views.py not found at", p.resolve())
    sys.exit(1)

# backup
bak = p.with_suffix(p.suffix + f".bak_fix_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}")
shutil.copy2(p, bak)
print("Backup created:", bak)

text = p.read_text(encoding="utf8")

# Pattern: optional decorators above the def, the def line, and its indented body until the next top-level def or EOF
pattern = re.compile(
    r"""(?mx)                      # multiline, verbose
    (^[ \t]*@.*\r?\n)*             # optional decorator lines (0..n)
    ^[ \t]*def[ \t]+freelancer_payment_overview\s*\([^\)]*\)\s*:\s*\r?\n  # def line
    (?:[ \t].*(?:\r?\n|$))*        # indented function body lines (0 or more)
    (?=(^[ \t]*def[ \t]+\w+\s*\(|\Z))  # stop before next top-level def or EOF
    """
)

m = pattern.search(text)
if not m:
    print("Could not locate freelancer_payment_overview(...) in freelancer/views.py — no change made.")
    sys.exit(0)

start, end = m.span()
print("Found freelancer_payment_overview() block -- replacing with safe stub.")

stub = (
    "@login_required\n"
    "def freelancer_payment_overview(request):\n"
    "    \"\"\"Payment views removed. This stub keeps the app running and redirects users.\"\"\"\n"
    "    try:\n"
    "        from django.shortcuts import redirect\n"
    "        return redirect('freelancer_profile')\n"
    "    except Exception:\n"
    "        from django.http import HttpResponse\n"
    "        return HttpResponse('Payments removed', status=200)\n\n"
)

new_text = text[:start] + stub + text[end:]
p.write_text(new_text, encoding="utf8")
print("Replacement written to freelancer/views.py")
print("Now run: python manage.py runserver")
