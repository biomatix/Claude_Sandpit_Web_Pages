# Preview generator for the Malanda Rainbowfish (Melanotaenia sp. nov. "Malanda"), an
# UNDESCRIBED, Critically Endangered species. Prose written originally from Unmack et al.
# (2016) "Malanda Gold" and Martin & Barclay (2023), Fishes of Sahul. Figures rendered via
# pixmap (correct orientation). Not yet wired into the build / menu.
import os, html, build

OUT = os.path.join(build.SRC, "rainbowfish_species")
SLUG = "melanotaenia_malanda"
TITLE = "Malanda Rainbowfish"
GEN = '<span class="scientific-name">Melanotaenia</span>'
NAME = GEN + ' sp. &ldquo;Malanda&rdquo;'      # partial italic: genus only

def fig(fn, desc, credit):
    cap = "Malanda Rainbowfish"
    if desc:
        cap += " &mdash; " + html.escape(desc)
    cap += " &mdash; photo &copy; " + html.escape(credit)
    return ('      <div class="image-block"><img src="%s" alt="Malanda Rainbowfish">'
            '<div class="image-caption">%s</div></div>' % (fn, cap))

def h2(t): return "      <h2>%s</h2>" % t
def p(t):  return "      <p>%s</p>" % t
def sp(n): return '<span class="scientific-name">%s</span>' % n

parts = []
parts.append(fig("melanotaenia_malanda_hero.jpg",
                 "male in full breeding colour, unnamed creek at Wallace Road, Atherton Tablelands", "Keith Martin"))
parts.append('      <h1>%s</h1>' % NAME)
parts.append('      <p class="author-citation">Undescribed species &mdash; awaiting formal description</p>')
parts.append('      <p class="common-name">Malanda Rainbowfish</p>')

parts.append(h2("Species Summary"))
parts.append(p(
    "The Malanda Rainbowfish is a small, gold-and-red rainbowfish endemic to the Wet Tropics of "
    "north Queensland, Australia. It is a genuinely distinct species &mdash; confirmed by genetic "
    "and meristic study &mdash; but it has <strong>not yet been formally described or named</strong>, "
    "and so is referred to as %s. It is one of the smallest Australian rainbowfishes and one of very "
    "few restricted to high-elevation streams, living only in a handful of cool upland creeks on the "
    "Atherton Tablelands. Long confused in the aquarium hobby with the Lake Eacham Rainbowfish (%s) "
    "and the Utchee Rainbowfish (%s), and known informally by names such as &ldquo;Malanda Gold&rdquo;, "
    "&ldquo;Upland Utchee&rdquo; and &ldquo;Tarzali&rdquo; Rainbowfish, it is now recognised as a "
    "member of the Australis group of rainbowfishes. It is listed as <strong>Critically "
    "Endangered</strong> on both the IUCN Red List and under Australia&rsquo;s EPBC Act, and is at "
    "serious risk of extinction before it can even be named." % (
        NAME, sp("Melanotaenia eachamensis"), sp("Melanotaenia utcheensis"))))

parts.append(fig("melanotaenia_malanda_male_williams.jpg",
                 "“Malanda Gold” male from Williams Creek, part of the core range", "Keith Martin"))

parts.append(h2("Appearance"))
parts.append(p(
    "The Malanda Rainbowfish is a dwarf species with a notably short, deep body that gives it a "
    "rather stocky look, a rounded &ldquo;bull-nosed&rdquo; head and a large eye set close to the "
    "snout &mdash; quite unlike the pointed profile of the Eastern Rainbowfish (%s). Males carry a "
    "tall, flag-like first dorsal fin and square-cut second dorsal and anal fins that, unlike those "
    "of the Lake Eacham Rainbowfish, never overlap the tail base. The body is a brown-golden colour "
    "with narrow orange to brown stripes, intensifying in the breeding season to a bright golden "
    "yellow with fine red stripes and reddish dorsal, anal and caudal fins, the fins often edged in "
    "black. Females are more oval-bodied with a triangular first dorsal fin and are silver-brown with "
    "paler orange-brown stripes." % sp("Melanotaenia splendida splendida")))

parts.append(fig("melanotaenia_malanda_pair.jpg", "male (front) and female, Butchers Creek", "Keith Martin"))

parts.append(h2("Distribution &amp; Habitat"))
parts.append(p(
    "The species is named for the town of Malanda, and its core range is a small number of upper "
    "tributaries of the North Johnstone River on the southern Atherton Tablelands, at high elevations "
    "of about 650&ndash;800&nbsp;m. Extensive surveys have found it in only three creek systems there "
    "&mdash; the Ithaca River and its tributaries, Williams Creek, and a small unnamed creek at "
    "Wallace Road &mdash; and its range within those has been contracting to the uppermost reaches. "
    "In December 2021 it was discovered at a fourth site, Butchers Creek, in rainforest adjoining "
    "Gadgarra National Park; this record is especially notable because Butchers Creek lies in the "
    "neighbouring Mulgrave-Russell drainage basin, entirely separate from the North Johnstone. The "
    "streams it lives in are small, cool (about 16&ndash;22&nbsp;&deg;C) and fast-flowing, over a "
    "base of basalt bedrock, boulders and cobbles with red silt, and are often broken by low vertical "
    "waterfalls. There is little aquatic vegetation beyond occasional %s and the Queensland Lace "
    "Plant (%s)." % (sp("Blyxa aubertii"), sp("Aponogeton bullosus"))))

parts.append(fig("melanotaenia_malanda_habitat.jpg",
                 "Butchers Creek: basalt-based upland stream in rainforest", "Keith Martin"))

parts.append(h2("Conservation"))
parts.append(p(
    "The greatest threat to the Malanda Rainbowfish is hybridisation with the Eastern Rainbowfish "
    "(%s), a larger, widely translocated native fish that has invaded much of its range; where the "
    "two meet they interbreed, swamping and genetically diluting the smaller species until pure "
    "Malanda Rainbowfish survive only above barriers such as small causeways and waterfalls. "
    "Introduced fishes &mdash; Eastern Gambusia (%s), tilapia and Guppies (%s) &mdash; and the "
    "clearing of the surrounding rainforest for dairy and cattle farming add further pressure. "
    "Surveys have documented a rapid, ongoing contraction of the species&rsquo; range, which is why "
    "it is assessed as Critically Endangered." % (
        sp("Melanotaenia splendida splendida"), sp("Gambusia holbrooki"), sp("Poecilia reticulata"))))

parts.append(fig("melanotaenia_malanda_voucher.jpg",
                 "preserved museum voucher specimen (male), Northern Territory Museum", "Michael Hammer"))

parts.append(h2("Taxonomy &amp; Names"))
parts.append(p(
    "The Malanda Rainbowfish belongs to the Australis group, a lineage of closely related Australian "
    "and New Guinean rainbowfishes. The upper North Johnstone catchment is remarkable for holding "
    "several members of this single group &mdash; including the Eastern, Lake Eacham, Utchee and "
    "&ldquo;Tully&rdquo; Rainbowfishes &mdash; which do not normally co-exist without hybridising, and "
    "this tangle is a large part of why the Malanda form went so long unrecognised. Early genetic "
    "studies variously assigned its populations to the Lake Eacham Rainbowfish or, later, to the "
    "Utchee Rainbowfish, and the fish circulated under informal names such as &ldquo;Upland "
    "Utchee&rdquo;, &ldquo;Tarzali&rdquo; and &ldquo;Ithaca&rdquo; Rainbowfish. Modern genome-wide "
    "sequencing has since shown it to be a distinct species; a formal description is in preparation "
    "but had not been published at the time these sources were written."))

parts.append(p('      <em>Account compiled for Home of the Rainbowfish from P.&nbsp;J.&nbsp;Unmack, '
               'K.&nbsp;Martin, M.&nbsp;P.&nbsp;Hammer, B.&nbsp;Ebner, K.&nbsp;Moy &amp; '
               'C.&nbsp;Brown (2016), &ldquo;Malanda Gold&rdquo;, Fishes of Sahul 30(4), and '
               'K.&nbsp;C.&nbsp;Martin &amp; S.&nbsp;Barclay (2023), Fishes of Sahul 37(1): '
               '1994&ndash;2000 (Australia New Guinea Fishes Association).</em>'))

page = build.render_page(
    TITLE, "\n".join(parts), active_slug="rainbowfish_species", prefix="../",
    breadcrumb=['<a href="rainbowfish_species.html">Rainbowfish Species</a>',
                '%s sp. &ldquo;Malanda&rdquo;' % GEN])
build.write(os.path.join(OUT, SLUG + ".html"), page)
print("wrote", SLUG + ".html")
