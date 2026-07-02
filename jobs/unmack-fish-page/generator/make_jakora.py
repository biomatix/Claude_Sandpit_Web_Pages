# Preview generator for the new Melanotaenia jakora account (not yet wired into the
# build / menu). Reuses build.render_page so the chrome + CSS match real accounts.
# Prose is written originally from the two Fishes of Sahul (2023) articles; images are
# credited to their photographers. The Google-Earth map is deliberately omitted.
import os, html, build

BINOM = "Melanotaenia jakora"
OUT = os.path.join(build.SRC, "rainbowfish_species")

def fig(fn, desc, credit):
    cap = '<span class="scientific-name">%s</span>' % html.escape(BINOM)
    if desc:
        cap += " &mdash; " + html.escape(desc)
    cap += " &mdash; photo &copy; " + html.escape(credit)
    return ('      <div class="image-block"><img src="%s" alt="%s">'
            '<div class="image-caption">%s</div></div>' % (fn, html.escape(BINOM), cap))

def h2(t):
    return "      <h2>%s</h2>" % t

def p(t):
    return "      <p>%s</p>" % t

SN = '<span class="scientific-name">%s</span>'
def sp(name):
    return SN % name

parts = []
parts.append(fig("melanotaenia_jakora_male.jpg", "adult males, aquarium", "Erwin Binner"))
parts.append('      <h1><span class="scientific-name">%s</span></h1>' % html.escape(BINOM))
parts.append('      <p class="author-citation">Graf, Ohee, Herder &amp; Haryono, 2023</p>')
parts.append('      <p class="common-name">Jakora Rainbowfish</p>')

parts.append(h2("Species Summary"))
parts.append(p(
    "%s is a small, slender rainbowfish described in 2023 from the southern Vogelkop "
    "(Bird&rsquo;s Head) Peninsula of Papua Barat Province, in western New Guinea "
    "(Indonesia). It is a modest fish, reaching only about 65&nbsp;mm in standard length, "
    "but the males are strikingly coloured. The back is blackish-brown, grading to brown "
    "along the upper flanks, and is crossed by a bold dark midlateral stripe two scale-rows "
    "deep with a whitish-silver stripe beneath it. In direct light the whole body takes on "
    "an iridescent blue sheen; the lower part of the gill cover is red and the fins carry "
    "bluish-white margins. The unpaired fins of adult males are moderately elongated, their "
    "tips reaching back to the base of the tail. Females are plainer &mdash; brown with a "
    "dark midlateral stripe and faint orange stripes low on the body. Genetic analysis "
    "indicates that %s is a distinct lineage, not closely allied to the other rainbowfishes "
    "of the Vogelkop Peninsula and most closely related to the wider Bird&rsquo;s Head "
    "lineage. It was known to aquarists before it was formally named, under the interim "
    "label %s." % (sp(BINOM), sp(BINOM), sp('Melanotaenia') + ' sp. &ldquo;Kali Jakora&rdquo;')))

parts.append(fig("melanotaenia_jakora_female.jpg", "female, aquarium", "Erwin Binner"))

parts.append(h2("Distribution &amp; Habitat"))
parts.append(p(
    "%s is known only from the vicinity of Meyado and Jakora village in the Sebjar "
    "(Sungai Sebjar) River system, in the southern part of the Vogelkop Peninsula, Papua "
    "Barat Province, Indonesia, and appears to be endemic to that small area. The type "
    "series was collected in August 2017 from a shaded rainforest creek crossing the road "
    "between Meyado and Jakora &mdash; a blackwater habitat stained dark with tannins, with "
    "a muddy substrate and no submerged aquatic plants. The water was soft and acidic: about "
    "26&nbsp;&deg;C, conductivity around 30&nbsp;&micro;S, pH 6.4, and hardness below the "
    "limit of measurement. The only other fish recorded alongside it was an undescribed "
    "%s of the local Vogelkop group." % (sp(BINOM), sp("Melanotaenia"))))

parts.append(fig("melanotaenia_jakora_habitat.jpg",
                 "type locality: blackwater creek near Jakora, Sebjar River system",
                 "Henderite L. Ohee"))

parts.append(h2("Description"))
parts.append(p(
    "A small species, adults less than 65&nbsp;mm SL, with a slender body (body depth about "
    "3.4 times in standard length). The dorsal fin has IV (III&ndash;V) spines followed by "
    "I,10 (I,9&ndash;12) soft rays; the anal fin has I,20 (18&ndash;22) rays; pectoral rays "
    "13; pelvic I,5; and the caudal fin has 15 branched rays. There are 37 (35&ndash;39) "
    "lateral scales, 21 (18&ndash;25) predorsal scales, and 14 (11&ndash;17) gill rakers on "
    "the first arch. In adult males the dorsal and anal fins are elongated, their tips "
    "reaching the base of the caudal fin. The species is distinguished from other Vogelkop "
    "rainbowfishes by this combination of counts together with the male colour &mdash; scales "
    "without dark margins, a reflective blue body sheen, and an unbroken midlateral stripe. "
    "In body shape it most resembles the Australian %s, but it differs consistently in its "
    "fin-ray and scale counts." % sp("Melanotaenia gracilis")))

parts.append(fig("melanotaenia_jakora_group.jpg", "group of males, aquarium", "Johannes Graf"))

parts.append(h2("Keeping &amp; Caring"))
parts.append(p(
    "In the aquarium %s is a peaceful, rather retiring rainbowfish that does not compete well "
    "with more boisterous tankmates, so a single-species tank suits it best. Given soft, "
    "humic-rich water at around 25&nbsp;&deg;C, moderate lighting from the front, and a "
    "layout of driftwood and some plants, the males display their iridescent colours to full "
    "effect and their courtship is a highlight. Like most small rainbowfishes the species is "
    "short-lived &mdash; roughly two years &mdash; so it is worth keeping young fish coming "
    "on, for example by providing floating plants or dense Java moss in which fry can find "
    "refuge. Sexual maturity is reached at about six months of age." % sp(BINOM)))

parts.append(h2("Breeding"))
parts.append(p(
    "%s spawns readily on a mop of synthetic yarn in soft, slightly acidic water, but rearing "
    "the eggs proved unusually demanding. Early attempts failed because the eggs turned white "
    "and died in ordinary, moderately hard water; success came only after the blackwater "
    "conditions of the type locality were reproduced. The breeders eventually established that "
    "it was the low pH &mdash; not the humic substances themselves &mdash; that mattered, with "
    "eggs developing only at roughly pH 4 to pH 5. The eggs are clear when laid and darken to "
    "light brown as they develop, hatching in about 8&ndash;10 days depending on temperature. "
    "Newly hatched larvae take infusoria at first and then brine shrimp nauplii. After several "
    "captive generations the line appears to be domesticating, with recent broods hatching "
    "successfully in softer water up to about pH 6.5." % sp(BINOM)))

parts.append(fig("melanotaenia_jakora_fry.jpg", "newly hatched fry", "Johannes Graf"))

parts.append(h2("Remarks"))
parts.append(p(
    "The species is named after Jakora village, the nearest named locality to the type site; "
    "the creek itself was known locally as &ldquo;Kali Jakora&rdquo;. It reached hobbyists "
    "before it was formally described, under the interim name %s, and because of its "
    "demanding blackwater breeding requirements it has so far remained uncommon in the hobby. "
    "As with many New Guinea rainbowfishes, its natural habitat is under pressure from "
    "deforestation, which adds conservation value to maintaining the species in aquaria." %
    (sp('Melanotaenia') + ' sp. &ldquo;Kali Jakora&rdquo;')))

parts.append(p('<em>Account compiled for Home of the Rainbowfish from J.&nbsp;A.&nbsp;Graf, '
               'H.&nbsp;L.&nbsp;Ohee, F.&nbsp;Herder &amp; Haryono (2023) and '
               'J.&nbsp;A.&nbsp;Graf (2023), Fishes of Sahul 37(2): 2063&ndash;2072 '
               '(Australia New Guinea Fishes Association).</em>'))

page = build.render_page(
    BINOM, "\n".join(parts), active_slug="rainbowfish_species", prefix="../",
    breadcrumb=['<a href="rainbowfish_species.html">Rainbowfish Species</a>',
                '<span class="scientific-name">%s</span>' % html.escape(BINOM)])
build.write(os.path.join(OUT, "melanotaenia_jakora.html"), page)
print("wrote", os.path.join(OUT, "melanotaenia_jakora.html"))
