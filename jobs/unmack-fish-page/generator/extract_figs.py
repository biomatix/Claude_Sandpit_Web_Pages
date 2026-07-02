# Re-extract new-species figures by RENDERING the page region (pixmap clip), which
# respects the page transform. Some of these Fishes of Sahul PDFs store their images
# upside-down and flip them upright via the page matrix, so raw extract_image() bytes
# come out inverted. Rendering the clip is orientation-correct for any PDF.
import os, fitz, build

OUT = os.path.join(build.SRC, "rainbowfish_species")
JAK = ("New_species_accounts/jakora/FOS Vol37No2 December 2023 A new rainbowfish "
       "Melanotaenia jakora.pdf")
JAK_DISC = ("New_species_accounts/jakora/FOS Vol37No2 December 2023 The discovery of "
            "Melanotaenia jakora.pdf")
GAR = "New_species_accounts/garylangei/FOSVol31No1 M. garylangei.pdf"
BASE = build.JOB

def render(pdf_rel, page, xref, out_name, dpi=200):
    doc = fitz.open(os.path.join(BASE, pdf_rel))
    p = doc[page - 1]
    bbox = None
    for im in p.get_image_info(xrefs=True):
        if im["xref"] == xref:
            bbox = fitz.Rect(im["bbox"]); break
    if bbox is None:
        raise SystemExit("xref %d not found on p%d of %s" % (xref, page, pdf_rel))
    pix = p.get_pixmap(clip=bbox, dpi=dpi)
    path = os.path.join(OUT, out_name)
    pix.save(path)                       # png
    # convert png->jpg for consistency with the site
    from PIL import Image
    import io
    im = Image.open(path).convert("RGB")
    jpg = out_name.rsplit(".", 1)[0] + ".jpg"
    im.save(os.path.join(OUT, jpg), "JPEG", quality=90)
    if not out_name.endswith(".jpg"):
        os.remove(path)
    print("%-42s %dx%d" % (jpg, im.width, im.height))

# --- garylangei (2017 discovery/keeping article, all photos © Gary Lange) ---
render(GAR, 7, 23, "melanotaenia_garylangei_male.jpg")
render(GAR, 9, 29, "melanotaenia_garylangei_adult.jpg")
render(GAR, 9, 30, "melanotaenia_garylangei_adult2.jpg")
render(GAR, 8, 27, "melanotaenia_garylangei_juvenile.jpg")
render(GAR, 3,  9, "melanotaenia_garylangei_habitat.jpg")

# --- jakora (re-rendered the same way for safety) ---
render(JAK, 1, 741, "melanotaenia_jakora_male.jpg")
render(JAK, 4,  11, "melanotaenia_jakora_female.jpg")
render(JAK, 7,  28, "melanotaenia_jakora_habitat.jpg")
render(JAK_DISC, 5, 29, "melanotaenia_jakora_group.jpg")
render(JAK_DISC, 5, 31, "melanotaenia_jakora_fry.jpg")
