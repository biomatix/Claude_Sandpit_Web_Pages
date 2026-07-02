# Render every new-species figure by RENDERING the page region (pixmap clip), which
# respects the page transform. Some Fishes of Sahul PDFs store their images upside-down
# and flip them upright via the page matrix, so raw extract_image() bytes come out
# inverted; rendering the clip is orientation-correct for any PDF.
import os, io, fitz, build
from PIL import Image

RF = os.path.join(build.SRC, "rainbowfish_species")
BE = os.path.join(build.SRC, "blue_eye_species")
BASE = build.JOB
NSA = "New_species_accounts"

JAK = NSA + "/jakora/FOS Vol37No2 December 2023 A new rainbowfish Melanotaenia jakora.pdf"
JAK_DISC = NSA + "/jakora/FOS Vol37No2 December 2023 The discovery of Melanotaenia jakora.pdf"
GAR = NSA + "/garylangei/FOSVol31No1 M. garylangei.pdf"
KIU = NSA + "/kiunga/FOS Vol38No2 June 2024 Kiunga revision.pdf"
MAN_D = NSA + "/mangrove/FOS Vol38No2 June 2024 Mangrove Blue-eye description.pdf"
MAN_C = NSA + "/mangrove/FOS Vol38No2 June 2024 Mangrove Blue-eye aquarium.care.pdf"
MAL_A = NSA + "/malanda/FOS Vol37No1 March 2023 Malanda Rainbows article.pdf"
MAL_B = NSA + "/malanda/FOSVol30No4 Malanda Rainbowfish.pdf"

def render(pdf_rel, page, xref, out_dir, name, dpi=200):
    doc = fitz.open(os.path.join(BASE, pdf_rel))
    p = doc[page - 1]
    bbox = next((fitz.Rect(im["bbox"]) for im in p.get_image_info(xrefs=True)
                 if im["xref"] == xref), None)
    if bbox is None:
        raise SystemExit("xref %d not found on p%d of %s" % (xref, page, pdf_rel))
    tmp = os.path.join(out_dir, "_tmp_render.png")
    p.get_pixmap(clip=bbox, dpi=dpi).save(tmp)
    im = Image.open(tmp).convert("RGB"); os.remove(tmp)
    im.save(os.path.join(out_dir, name), "JPEG", quality=90)

# --- garylangei (2017 discovery/keeping article, all photos © Gary Lange) ---
render(GAR, 7, 23, RF, "melanotaenia_garylangei_male.jpg")
render(GAR, 9, 29, RF, "melanotaenia_garylangei_adult.jpg")
render(GAR, 9, 30, RF, "melanotaenia_garylangei_adult2.jpg")
render(GAR, 8, 27, RF, "melanotaenia_garylangei_juvenile.jpg")
render(GAR, 3,  9, RF, "melanotaenia_garylangei_habitat.jpg")

# --- jakora ---
render(JAK, 1, 741, RF, "melanotaenia_jakora_male.jpg")
render(JAK, 4,  11, RF, "melanotaenia_jakora_female.jpg")
render(JAK, 7,  28, RF, "melanotaenia_jakora_habitat.jpg")
render(JAK_DISC, 5, 29, RF, "melanotaenia_jakora_group.jpg")
render(JAK_DISC, 5, 31, RF, "melanotaenia_jakora_fry.jpg")

# --- Kiunga (2024 revision) -> blue-eye section ---
render(KIU, 12, 39, BE, "kiunga_auromarginata_live.jpg")
render(KIU, 12, 41, BE, "kiunga_auromarginata_holotype.jpg")
render(KIU, 13, 45, BE, "kiunga_auromarginata_habitat.jpg")
render(KIU, 14, 49, BE, "kiunga_filamentosa_holotype.jpg")
render(KIU, 16, 55, BE, "kiunga_leucozona_live.jpg")
render(KIU, 17, 59, BE, "kiunga_leucozona_holotype.jpg")
render(KIU, 18, 63, BE, "kiunga_leucozona_habitat.jpg")

# --- Mangrove Blue-eye (Pseudomugil halophilus) -> blue-eye section ---
render(MAN_D,  9, 23, BE, "pseudomugil_halophilus_live.jpg")
render(MAN_D, 11, 29, BE, "pseudomugil_halophilus_fresh.jpg")
render(MAN_D, 14, 41, BE, "pseudomugil_halophilus_comparison.jpg")
render(MAN_D, 12, 33, BE, "pseudomugil_halophilus_holotype.jpg")
render(MAN_D, 15, 45, BE, "pseudomugil_halophilus_habitat.jpg")
render(MAN_C,  3, 37, BE, "pseudomugil_halophilus_juvenile.jpg")

# --- Malanda Rainbowfish (undescribed Melanotaenia) -> rainbowfish section ---
render(MAL_B, 1,  3, RF, "melanotaenia_malanda_hero.jpg", dpi=300)
render(MAL_A, 7, 29, RF, "melanotaenia_malanda_pair.jpg")
render(MAL_B, 2,  6, RF, "melanotaenia_malanda_male_williams.jpg")
render(MAL_A, 5, 18, RF, "melanotaenia_malanda_habitat.jpg")
render(MAL_A, 7, 31, RF, "melanotaenia_malanda_voucher.jpg")

print("extracted all new-species figures")
