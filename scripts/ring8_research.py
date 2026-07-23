#!/usr/bin/env python3
"""
Ring 8 affiliate outreach research — collect NEW email contacts for Focus Dock.

Goal: up to ~1000 new verified emails not already in master / prior batches / send log.

Sources:
  1. Notion Marketplace (deeper pages + more categories + template search)
  2. Gumroad Discover (expanded ADHD/Notion/productivity queries)
  3. Substack / Beehiiv about pages (large seed list)
  4. Podcast + coach site contact pages
  5. YouTube-adjacent creator sites

Usage:
  python scripts/ring8_research.py                 # full run, save batch
  python scripts/ring8_research.py --dry-run
  python scripts/ring8_research.py --limit 1000
"""

from __future__ import annotations

import argparse
import json
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from html import unescape
from pathlib import Path
from urllib.parse import urljoin, urlparse, quote

import urllib.request

ROOT = Path(__file__).parent.parent
MARKETING = ROOT / "marketing"
MASTER = MARKETING / "affiliate-contacts-master.json"
SEND_LOG = MARKETING / "email-send-log.json"
OUT = MARKETING / "_batch_ring8_expansion.json"

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)
EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}")
SKIP_EMAILS = {
    "templates@makenotion.com",
    "support@substack.com",
    "hello@substack.com",
    "noreply@stuartridout.com",
    "team@beehiiv.com",
    "support@gumroad.com",
    "help@gumroad.com",
    "privacy@notion.so",
    "hello@notion.so",
    "team@notion.so",
}
SKIP_EMAIL_DOMAINS = {
    "substack.com",
    "beehiiv.com",
    "gumroad.com",
    "notion.so",
    "makenotion.com",
    "sentry.io",
    "wixpress.com",
    "example.com",
    "cloudfront.net",
    "listennotes.com",
}
WORKERS = 14
RESEARCH_RING = 8

# All known Notion template categories + extras
NOTION_CATEGORIES = [
    "personal-productivity", "personal-dashboards", "second-brain", "health-fitness",
    "personal-finance", "hobbies", "travel", "food-nutrition", "career-building",
    "parenting", "entertainment", "housing", "dating-relationships", "friends-family",
    "seasonal", "religion", "plants", "vehicle-management",
    "startup", "freelance", "side-hustle", "product", "marketing", "design", "engineering",
    "ai", "operations", "hr", "work-dashboards", "recruiting", "it", "sales", "crm",
    "user-research", "data-science", "finance", "pr-comms", "enterprise", "managers",
    "non-profit", "agency", "consulting", "venture-capital", "website-building", "integrations",
    "student-life", "study-planner", "class-notes", "student-dashboards", "student-org",
    "teaching", "school-applications", "internship-tracker", "academic-research",
    "personal", "work", "school", "meetings", "project-management", "wiki",
    "docs", "knowledge-base", "okrs", "roadmap", "bugs", "sprints",
    "content-calendar", "social-media", "creator", "influencer", "podcast",
    "writing", "journaling", "habits", "goals", "reading", "recipes",
]

NOTION_SEARCH_QUERIES = [
    "adhd", "adhd planner", "adhd dashboard", "neurodivergent", "executive function",
    "second brain", "life os", "lifeos", "pkm", "productivity", "habit tracker",
    "daily planner", "weekly planner", "task manager", "focus", "dopamine",
    "student planner", "teacher planner", "content creator", "youtube planner",
    "freelancer", "solopreneur", "coach", "therapy notes", "mental health",
    "bullet journal", "time blocking", "pomodoro", "gtd", "para method",
    "atomic habits", "notion calendar", "meeting notes", "crm", "startup os",
    "personal dashboard", "home dashboard", "finance tracker", "budget",
    "reading list", "book tracker", "journal", "gratitude", "mood tracker",
    "workout", "fitness", "meal planner", "recipe", "travel planner",
    "wedding planner", "parenting", "homeschool", "study", "exam",
    "job search", "resume", "portfolio", "design system", "brand kit",
    "social media planner", "newsletter", "podcast planner", "video planner",
    "affiliate", "business planner", "okrs", "sprint", "project tracker",
    "knowledge base", "wiki", "notes", "zettelkasten", "obsidian alternative",
    "minimalist", "aesthetic", "pastel", "dark mode", "dashboard 2024",
    "dashboard 2025", "dashboard 2026", "new year", "reset", "reset planner",
    "adhd adult", "adhd women", "adhd kids", "autism", "audhd",
    "body doubling", "accountability", "routine", "morning routine",
    "evening routine", "brain dump", "capture", "inbox zero",
]

GUMROAD_QUERIES = [
    "adhd", "notion templates", "notion planner", "productivity planner",
    "neurodivergent", "second brain notion", "adhd planner", "notion dashboard",
    "executive function", "digital planner", "notion life os", "pkm notion",
    "habit tracker notion", "adhd coaching", "notion adhd", "notion productivity",
    "adhd notion template", "planner template", "notion second brain",
    "goodnotes planner", "ipad planner", "digital notebook", "undated planner",
    "hyperfocus", "dopamine menu", "body doubling", "time blindness",
    "notion crm", "notion student", "notion teacher", "notion creator",
    "content calendar notion", "youtube notion", "freelance notion",
    "solopreneur", "life dashboard", "goal tracker", "habit journal",
    "bullet journal digital", "printable planner", "adhd worksheet",
    "adhd workbook", "executive function coach", "productivity coach",
    "notion aesthetic", "notion pastel", "notion dark", "minimal planner",
    "study planner", "exam planner", "homeschool planner", "meal planner digital",
    "budget planner digital", "finance tracker", "reading journal",
    "therapy journal", "mental health planner", "self care planner",
    "notion os", "all in one notion", "life operating system",
    "adhd adult", "adhd women planner", "neurospicy", "audhd planner",
    "pomodoro tracker", "focus timer", "deep work", "time block planner",
    "gtd template", "para method", "atomic notes", "zettelkasten digital",
    "creator economy", "newsletter planner", "podcast planner template",
    "course planner", "coaching client tracker", "client portal notion",
]

# Large Substack slug seed list (ADHD / Notion / productivity / coaching / PKM)
SUBSTACK_SEEDS = [
    "neurodiverseproductivity", "adhdunpacked", "kristenlynnmcclure", "extrafocus",
    "adhdjesse", "theadhddigest", "neurodivergentinsights", "theadhdwriter",
    "shimmeradhd", "adultingwithadhd", "executivedysfunction", "notionway",
    "notionthings", "pkmjournal", "secondbraindispatch", "productivitycafe",
    "theorganizedbrain", "divergentdispatch", "neurospicynotes", "focusfuel",
    "plannerbrain", "theadhdadvantage", "ndproductivity", "braindumpclub",
    "notionforcreators", "templateatlas", "digitalplannerhub", "calmclarityco",
    "mindfulproductivity", "theadhdentrepreneur", "spicybrain", "organizedadult",
    "notionnerd", "systemsandself", "thefocusfix", "dopaminediary",
    "neurodivergentcoach", "plannerpeace", "executivefunctioncoach", "notionobsessed",
    "adhdproductivity", "neurodivergentlife", "theadhdmom", "focuswithadhd",
    "productivitywithadhd", "notionplanner", "digitalbrain", "plannersociety",
    "neurodivergentnews", "adhdproductivitylab", "mindwithadhd",
    "adhdrewired", "hackingyouradhd", "translatingadhd", "adhdessentials",
    "theadhdacademy", "takecontroladhd", "adhdfriendlylifestyle", "adhdvision",
    "focusedadult", "myndsystems", "adhdlove", "authenticadhd", "adhddiversified",
    "impactparents", "learntotalkadhd", "beyondbooksmart", "adhdonline",
    "productivityist", "beyondthetodo", "systemsmadebetter", "getorganizedhq",
    "thomasfrank", "augustbradley", "easlonotes", "redgregory", "aliabdaal",
    "tiagoforte", "buildingasecondbrain", "fortelabs", "pkmweekly", "linkingyourthinking",
    "obsidianroundup", "notionmastery", "keepproductivenotion", "notionvip",
    "superorganizers", "every", "divinations", "readwise", "readreadread",
    "thesweetsetup", "macstories", "clubmacstories", "ruriohama", "ruri",
    "mariepoulin", "keepproductive", "productivedude", "carlpullein",
    "mikevardy", "asianefficiency", "zenhabits", "calnewport", "deepquestions",
    "jamesclear", "atomichabits", "theprocess", "makerpad", "nocode",
    "indiehackers", "levelsio", "pieterlevels", "justinwelsh", "dickiebush",
    "nicolascole", "ship30", "typeshare", "writeofpassage", "davidperell",
    "anniemurphy", "anniemurphypaul", "languagelog", "adhdwomen",
    "adhdactually", "adhdmess", "adhdandchill", "adhdisawesome", "adhdfriendly",
    "adhdparenting", "adhdkids", "adhdfamily", "adhdatwork", "adhdcareer",
    "adhdfinance", "adhdrelationships", "adhdmarriage", "adhdcouples",
    "neurospicy", "neurospicylife", "audhd", "audhdlife", "autisticandadhd",
    "execfunction", "workingmemory", "timeblind", "rejectiondsd",
    "dopaminedetox", "dopaminemenu", "bodydoubling", "adhdcoach",
    "adhdcoaching", "adhdcoaches", "productivitycoach", "focuscoach",
    "notioncoach", "templateclub", "plannerclub", "digitalplanning",
    "goodnotesclub", "ipadplanning", "notabilityplanner", "remarkable",
    "paperlessmovement", "gtdtimes", "gettingthingsdone", "facilethings",
    "todoistblog", "ticktick", "thingsapp", "omnifocus", "culturedcode",
    "notionblog", "notioneverything", "allthingnotion", "notionlife",
    "notionworkspace", "notionsetup", "notiontemplates", "freetemplates",
    "paidtemplates", "creatoreconomy", "creatorhq", "newsletterops",
    "beehiivblog", "convertkit", "kitblog", "substacknotes",
    "mindfultech", "digitalminimalism", "attentioneconomy", "focusmode",
    "deepworkdaily", "shallowwork", "makerschedule", "managerschedule",
    "solopreneurlife", "onepersonbusiness", "indiebusiness", "bootstrapped",
    "sidehustlenews", "freelancewriting", "freelancecoach", "consultingclub",
    "adhdtherapist", "adhdtherapy", "neuroaffirming", "strengthsbasedadhd",
    "adhdstudent", "adhdcollege", "adhdgrad", "adhdatuni",
    "adhdteacher", "adhdclassroom", "inclusiveclassroom", "udl",
    "adhdmomlife", "adhdadulthood", "lateadhd", "lateadhddiagnosis",
    "womenwithadhd", "adhdinwomen", "girlsandwomenwithadhd",
    "adhddad", "adhdmen", "menwithadhd", "adhdandwork",
    "burnoutrecovery", "adhdandburnout", "restisproductive",
    "habitstacking", "tinyhabits", "atomicnotes", "fleetingnotes",
    "evergreennotes", "smartnotes", "howtotakenotes", "notetaking",
    "secondbrainlab", "basblab", "codeandcreativity", "toolsforthought",
    "toolsforthought", "roamresearch", "logseq", "tana", "capacities",
    "craftnotes", "memai", "reflectnotes", "heynote",
    "planneraddict", "planningcommunity", "beforethepen", "planwithme",
    "planwith", "weeklyreset", "sundayreset", "monthlyreset",
    "quarterlyplanning", "annualplanning", "yearcompass",
    "adhdlifehacks", "adhdlifehack", "adhdtips", "adhdhacks",
    "productivityhacks", "notionhacks", "notiontips", "notiontricks",
    "theproductivityshow", "asianefficiencyblog", "beyondthetodolist",
    "gettingthingsdoneblog", "zenhabitsblog", "calnewportblog",
    "aliabdaalblog", "thomasfrankblog", "ruriohama notes",
    "adhdrewiredblog", "hackingadhd", "adhd2point0", "driven2distraction",
    "scattered", "scatteredminds", "deliveredfromdistraction",
    "smartbutscattered", "takingchargeadhd", "youmeandouradhds",
    "themindexplained", "brainandlife", "additudemag", "additude",
    "chadd", "adhdfoundation", "adhdeurope", "ukadhd",
    "adhdaust", "adhdcanda", "canadadhd",
    "focusmate", "flowclub", "caveday", "deepstash",
    "readwiseio", "matter", "instapaper", "pocket",
    "mynd", "shimmercare", "inflow", "inflowadhd", "sanvello",
    "headspace", "calmblog", "finchcare", "goblintools",
    "tiimo", "structuredapp", "juggle", "sorted3",
    "sunsama", "motion", "reclaimai", "clockwise",
    "akiflow", "superlist", "linearapp", "heightapp",
    "clickup", "asana", "mondaycom", "notionhq",
    "codaio", "airtable", "fibery", "trello",
    "adhdcollective", "theadhdcollective", "adhddispatch",
    "weeklyadhd", "dailyadhd", "adhddaily", "adhdigest",
    "notionweekly", "pkmclub", "secondbrainclub", "basbclub",
    "templatefoundry", "templatecraft", "templatemarket",
    "digitalgoods", "printableshop", "etsydigital", "gumroadcreators",
    "creativefocus", "creativeadhd", "artistadhd", "writeradhd",
    "entrepreneuradhd", "founderwithadhd", "startupadhd",
    "remoteadhd", "wfhwithadhd", "asyncwork", "deepworkremote",
    "parentswithadhd", "raisingadhd", "adhdfamily life",
    "spousewithadhd", "partnerwithadhd", "datingwithadhd",
    "adhdandanxiety", "adhdanddepression", "comorbid",
    "rejection sensitivity", "rsd", "emotionaldysregulation",
    "rejectiondsd", "emotionalregulationadhd",
    "sleepandadhd", "adhdinsomnia", "circadianadhd",
    "exerciseadhd", "movementadhd", "adhdandfitness",
    "nutritionadhd", "adhdandfood", "dopaminefood",
    "medsandadhd", "adhdmeds", "stimulantlife",
    "unmedicatedadhd", "naturaladhd", "adhdlifestyle",
    "adhdandmoney", "adhdspending", "financialadhd",
    "adhdandclutter", "messyadhd", "organizingadhd",
    "homewithadhd", "adhdcleaning", "bodydoublingclean",
    "adhdandtime", "timeperception", "deadlineadhd",
    "procrastinationadhd", "taskinitiation", "taskparalysis",
    "adhdparalysis", "analysisparalysis", "decisionfatigue",
    "adhddecision", "choiceoverload", "simpleadhd",
    "minimalistadhd", "adhdaesthetic", "cuteplanner",
    "pastelplanner", "cozyproductivity", "softproductivity",
    "gentleproductivity", "slowproductivity", "restfulwork",
    "antioptimization", "enoughness", "goodenough",
    "progressnotperfection", "doneisbetter", "shipit",
    "buildinpublic", "indiehackersweekly", "solohacker",
    "microstartup", "tinyproduct", "digitalproduct",
    "info product", "coursecreators", "cohortbased",
    "communitybuilders", "membership", "paidnewsletter",
    "substackwriters", "writerstack", "essayclub",
    "notetakers", "lifelonglearners", "curiousmind",
    "polymath", "generalist", "multipotentialite",
    "adhdspecialinterest", "hyperfixation", "hyperfocuslife",
    "flowstate", "flowchannel", "peakperformance",
    "highperformance", "elitehabits", "morningroutines",
    "eveningroutines", "winddown", "shutdownritual",
    "weeklyreview", "gtdweekly", "fridayreset", "mondaysetup",
    "kanbanlife", "personalkanban", "scrumlife",
    "agilelife", "leanlife", "continuousimprovement",
    "kaizen", "1percentbetter", "compoundgrowth",
    "identityhabits", "systemsnotgoals", "processoveroutcome",
    "environmentdesign", "choicearchitecture", "nudge",
    "behavioraldesign", "habitdesign", "routinescience",
    "attentionscience", "cognitivescience", "brainscience",
    "neurosciencehabits", "neuroplasticity", "braintraining",
    "workingmemorytraining", "focus training", "attentiontraining",
    "mindfulnessadhd", "meditationadhd", "mbct", "acttherapy",
    "cbtforadhd", "dbt skills", "radicallyopen",
    "selfcompassion", "innercritic", "shameandadhd",
    "adhdstigma", "neurodiversity", "neurodiversityatwork",
    "inclusivework", "accommodations", "workplaceadhd",
    "disclosureadhd", "askingforhelp", "selfadvocacy",
    "adhdadvocacy", "disabilityjustice", "accessneeds",
    "spoonie", "spoonies", "chronicillness", "comorbidchronic",
    "fatigueandadhd", "energymanagement", "spoons",
    "capacityplanning", "energybudget", "personalbandwidth",
    "contextswitching", "multitaskingmyth", "single tasking",
    "monotasking", "batching", "theme days", "makertuesdays",
    "adminfridays", "deepworkblocks", "focusblocks",
    "timetracking", "rescue time", "toggl", "clockify",
    "hours", "timular", "rize", "timingapp",
    "notionapi", "notionautomation", "make.com", "zapier",
    "n8n", "pipedream", "bardeen", "raycast",
    "alfredapp", "keyboardmaestro", "textexpander", "espanso",
    "obsidianmd", "obsidianplugins", "logseqnotes", "remnote",
    "anki", "spacedrepetition", "supermemo", "m//memory",
    "learninghowtolearn", "ultralearning", "scott young",
    "barbaraoakley", "coursera", "skillshare", "masterclass",
    "udemy", "teachable", "kajabi", "thinkific",
    "podia", "gumroadcreatorsclub", "lemonsqueezy",
    "paddle", "stripeatlas", "blacksheep",
]

BEEHIIV_SEEDS = [
    "adhd", "productivity", "notion", "neurodivergent", "focus",
    "planner", "habits", "secondbrain", "pkm", "creator",
    "solopreneur", "newsletter", "deepwork", "timemanagement",
]

PODCAST_SEEDS = [
    ("https://www.hackingyouradhd.com/", "Hacking Your ADHD", "William Curb"),
    ("https://www.translatingadhd.com/", "Translating ADHD", ""),
    ("https://www.adhdrewired.com/", "ADHD reWired", "Eric Tivers"),
    ("https://www.adhdforsmartasswomen.com/", "ADHD for Smart Ass Women", ""),
    ("https://www.adhdessentials.com/", "ADHD Essentials", "Brendan Mahan"),
    ("https://www.adhdfriendlylifestyle.com/", "ADHD Friendly Lifestyle", ""),
    ("https://www.adhdthriveinstitute.com/", "ADHD Thrive Institute", ""),
    ("https://www.focusedadult.com/", "Focused Adult", ""),
    ("https://www.myndforadhd.com/", "Mynd Systems For ADHD", ""),
    ("https://www.adhdvision.com/", "ADHD Vision", ""),
    ("https://www.thriveadhdcoach.co.uk/", "Thrive ADHD Coach", ""),
    ("https://www.beyondbooksmart.com/", "Beyond BookSmart", ""),
    ("https://www.adhd2bb.com/", "ADHD 2.0 and Beyond", ""),
    ("https://www.neurodivergentpodcast.com/", "Neurodivergent Podcast", ""),
    ("https://www.authenticadhd.com/", "Authentic ADHD", ""),
    ("https://www.adhdlove.com/", "ADHD Love", ""),
    ("https://www.adhdparentingpodcast.com/", "ADHD Parenting Podcast", ""),
    ("https://www.theadhdacademy.com/", "The ADHD Academy", ""),
    ("https://www.productivityist.com/", "Productivityist", "Mike Vardy"),
    ("https://www.beyondtheto-do.com/", "Beyond the To-Do List", "Erik Fisher"),
    ("https://www.thesystemsmadebetter.com/", "Systems Made Better", ""),
    ("https://www.getorganizedhq.com/", "Get Organized HQ", ""),
    ("https://www.learntotalkadhd.com/", "Learn to Talk ADHD", ""),
    ("https://www.adhddiversified.com/", "ADHD Diversified", ""),
    ("https://www.impactparents.com/", "ImpactParents ADHD", ""),
    ("https://www.adultingwithadhd.com/", "Adulting with ADHD", ""),
    ("https://www.theadultingadhd.com/", "The Adulting ADHD Podcast", ""),
    ("https://www.adhdonline.com/", "ADHD Online", ""),
    ("https://www.takecontroladhd.com/", "Take Control ADHD", ""),
    ("https://www.adhdfoundation.org/", "ADHD Foundation", ""),
    ("https://www.additudemag.com/", "ADDitude Magazine", ""),
    ("https://chadd.org/", "CHADD", ""),
    ("https://www.understood.org/", "Understood", ""),
    ("https://www.adhdcoaches.org/", "ADHD Coaches Organization", ""),
    ("https://www.iasp.info/", "International ADHD Professional", ""),
    ("https://www.adhdawarenessmonth.org/", "ADHD Awareness Month", ""),
    ("https://www.totallyadd.com/", "Totally ADD", ""),
    ("https://www.adhdeurope.eu/", "ADHD Europe", ""),
    ("https://www.attentiondeficit-disorder.net/", "Attention Deficit Disorder", ""),
    ("https://www.adhdonline.co.uk/", "ADHD Online UK", ""),
    ("https://www.adhduk.co.uk/", "ADHD UK", ""),
    ("https://www.adhdaustralia.org.au/", "ADHD Australia", ""),
    ("https://caddac.ca/", "CADDAC", ""),
    ("https://www.canadadhd.ca/", "CADDRA", ""),
    ("https://www.edgefoundation.org/", "Edge Foundation", ""),
    ("https://www.smartbutscatteredkids.com/", "Smart but Scattered", ""),
    ("https://www.drhallowell.com/", "Dr. Hallowell", ""),
    ("https://www.drnedhallowell.com/", "Ned Hallowell", ""),
    ("https://www.russellbarkley.org/", "Russell Barkley", ""),
    ("https://www.thomasfrank.com/", "Thomas Frank", ""),
    ("https://www.aliabdaal.com/", "Ali Abdaal", ""),
    ("https://www.ruriohama.com/", "Ruri Ohama", ""),
    ("https://easlo.gumroad.com/", "Easlo", ""),
    ("https://www.keepproductive.com/", "Keep Productive", ""),
    ("https://www.notion.vip/", "Notion VIP", ""),
    ("https://www.fortelabs.com/", "Forte Labs", "Tiago Forte"),
    ("https://www.buildingasecondbrain.com/", "Building a Second Brain", ""),
    ("https://www.asianefficiency.com/", "Asian Efficiency", ""),
    ("https://zenhabits.net/", "Zen Habits", "Leo Babauta"),
    ("https://www.calnewport.com/", "Cal Newport", ""),
    ("https://jamesclear.com/", "James Clear", ""),
    ("https://www.carlpullein.com/", "Carl Pullein", ""),
    ("https://www.mariepoulin.com/", "Marie Poulin", ""),
    ("https://www.augustbradley.com/", "August Bradley", ""),
    ("https://www.redgregory.com/", "Red Gregory", ""),
    ("https://www.notionmastery.com/", "Notion Mastery", ""),
    ("https://superorganizers.substack.com/", "Superorganizers", ""),
    ("https://every.to/", "Every", ""),
    ("https://www.thesweetsetup.com/", "The Sweet Setup", ""),
    ("https://www.focusmate.com/", "Focusmate", ""),
    ("https://www.flow.club/", "Flow Club", ""),
    ("https://www.caveday.org/", "Caveday", ""),
    ("https://www.inflowapp.com/", "Inflow", ""),
    ("https://www.gosimmer.com/", "Shimmer", ""),
    ("https://www.tiimoapp.com/", "Tiimo", ""),
    ("https://www.structured.app/", "Structured", ""),
    ("https://goblin.tools/", "Goblin Tools", ""),
    ("https://www.sunsama.com/", "Sunsama", ""),
    ("https://www.usemotion.com/", "Motion", ""),
    ("https://www.reclaim.ai/", "Reclaim", ""),
    ("https://www.akiflow.com/", "Akiflow", ""),
    ("https://www.todoist.com/", "Todoist", ""),
    ("https://ticktick.com/", "TickTick", ""),
    ("https://www.omnigroup.com/omnifocus", "OmniFocus", ""),
    ("https://culturedcode.com/things/", "Things", ""),
    ("https://www.readwise.io/", "Readwise", ""),
    ("https://obsidian.md/", "Obsidian", ""),
    ("https://logseq.com/", "Logseq", ""),
    ("https://reflect.app/", "Reflect", ""),
    ("https://capacities.io/", "Capacities", ""),
    ("https://tana.inc/", "Tana", ""),
    ("https://www.remnote.com/", "RemNote", ""),
    ("https://www.craft.do/", "Craft", ""),
    ("https://coda.io/", "Coda", ""),
    ("https://www.airtable.com/", "Airtable", ""),
    ("https://clickup.com/", "ClickUp", ""),
    ("https://asana.com/", "Asana", ""),
    ("https://www.make.com/", "Make", ""),
    ("https://zapier.com/", "Zapier", ""),
    ("https://n8n.io/", "n8n", ""),
    ("https://www.bardeen.ai/", "Bardeen", ""),
    ("https://raycast.com/", "Raycast", ""),
    ("https://www.alfredapp.com/", "Alfred", ""),
    ("https://www.productivitygame.com/", "Productivity Game", ""),
    ("https://www.howtoadhd.com/", "How to ADHD", "Jessica McCabe"),
    ("https://www.adhdrewired.com/podcast", "ADHD reWired Podcast", ""),
    ("https://www.theproductivityshow.com/", "The Productivity Show", ""),
    ("https://www.happymd.org/", "HappyMD ADHD", ""),
    ("https://www.adhdrollercoaster.org/", "ADHD Roller Coaster", "Gina Pera"),
    ("https://www.adhdsuccesstips.com/", "ADHD Success Tips", ""),
    ("https://www.adhdessentials.com/podcast", "ADHD Essentials Podcast", ""),
    ("https://www.ihasadhd.com/", "I Have ADHD Podcast", "Kristen Carder"),
    ("https://www.kristencarder.com/", "Kristen Carder", ""),
    ("https://www.adhdreimagined.com/", "ADHD Reimagined", ""),
    ("https://www.scatteredminds.com/", "Scattered Minds", ""),
    ("https://www.drlidiazelikman.com/", "Dr Lidia Zelikman", ""),
    ("https://www.adhdawesome.com/", "ADHD is Awesome", ""),
    ("https://www.pennypwilliams.com/", "Penny Williams", ""),
    ("https://www.parentingadhdandautism.com/", "Parenting ADHD & Autism", ""),
    ("https://www.succeedwithadhd.com/", "Succeed with ADHD", ""),
    ("https://www.adhdatwork.com/", "ADHD at Work", ""),
    ("https://www.adhdatworksolutions.com/", "ADHD at Work Solutions", ""),
    ("https://www.workwithadhd.com/", "Work with ADHD", ""),
    ("https://www.adhdcareercoach.com/", "ADHD Career Coach", ""),
    ("https://www.theadhdcoach.com/", "The ADHD Coach", ""),
    ("https://www.adhdcoaching.org/", "ADHD Coaching", ""),
    ("https://www.jeffcoaching.com/", "Jeff Copper ADHD", ""),
    ("https://www.digcoaching.com/", "DIG Coaching", ""),
    ("https://www.edgecoaching.com/", "Edge Coaching", ""),
    ("https://www.jstcoaching.com/", "JST Coaching", ""),
    ("https://www.adhdmindfully.com/", "ADHD Mindfully", ""),
    ("https://www.mindfuladhd.com/", "Mindful ADHD", ""),
    ("https://www.calmclarity.org/", "Calm Clarity", ""),
    ("https://www.theottoolbox.com/", "The OT Toolbox", ""),
    ("https://www.yourkidstable.com/", "Your Kids Table", ""),
    ("https://www.growinghandsonkids.com/", "Growing Hands-On Kids", ""),
    ("https://www.andnextcomesl.com/", "And Next Comes L", ""),
    ("https://www.lemonlimeadventures.com/", "Lemon Lime Adventures", ""),
    ("https://www.notimeforflashcards.com/", "No Time for Flash Cards", ""),
    ("https://www.thepathway2success.com/", "The Pathway 2 Success", ""),
    ("https://www.socialemotionalworkshop.com/", "Social Emotional Workshop", ""),
    ("https://www.counselorchelsey.com/", "Counselor Chelsey", ""),
    ("https://www.counselorup.com/", "Counselor Up", ""),
    ("https://www.schoolcounselingfiles.com/", "School Counseling Files", ""),
    ("https://www.teacherspayteachers.com/", "Teachers Pay Teachers", ""),
    ("https://www.cultofpedagogy.com/", "Cult of Pedagogy", ""),
    ("https://www.edutopia.org/", "Edutopia", ""),
    ("https://www.understood.org/en", "Understood.org", ""),
    ("https://www.ldonline.org/", "LD Online", ""),
    ("https://www.ncld.org/", "NCLD", ""),
    ("https://www.ldaamerica.org/", "LDA America", ""),
    ("https://www.smartkidswithld.org/", "Smart Kids with LD", ""),
    ("https://www.wrightslaw.com/", "Wrightslaw", ""),
    ("https://www.adhdparenting.com/", "ADHD Parenting", ""),
    ("https://www.empoweringparents.com/", "Empowering Parents", ""),
    ("https://www.positiveparentingsolutions.com/", "Positive Parenting Solutions", ""),
    ("https://www.ahaparenting.com/", "Aha Parenting", ""),
    ("https://www.handinhandparenting.org/", "Hand in Hand Parenting", ""),
    ("https://www.livesinthebalance.org/", "Lives in the Balance", "Ross Greene"),
    ("https://www.cpsconnection.com/", "CPS Connection", ""),
    ("https://www.explosivechild.com/", "The Explosive Child", ""),
    ("https://www.adhdmarriage.com/", "ADHD Marriage", "Melissa Orlov"),
    ("https://www.adhdandmarriage.com/", "ADHD and Marriage", ""),
    ("https://www.adhdrelationship.com/", "ADHD Relationship", ""),
    ("https://www.thecoupleclinic.com/", "The Couple Clinic", ""),
    ("https://www.adhdrollercoaster.org/podcast", "ADHD Roller Coaster Podcast", ""),
    ("https://www.fasterthanormal.com/", "Faster Than Normal", "Peter Shankman"),
    ("https://shankman.com/", "Peter Shankman", ""),
    ("https://www.petershankman.com/", "Peter Shankman Site", ""),
    ("https://www.adhdrewired.com/coaching", "ADHD reWired Coaching", ""),
    ("https://www.adhdessentials.com/coaching", "ADHD Essentials Coaching", ""),
    ("https://www.ihasadhd.com/coaching", "I Have ADHD Coaching", ""),
    ("https://www.kristencarder.com/coaching", "Kristen Carder Coaching", ""),
    ("https://www.adhdcoaches.org/find-a-coach", "Find ADHD Coach", ""),
    ("https://www.paddc.org/", "PADDA", ""),
    ("https://www.adhdsupport.org/", "ADHD Support", ""),
    ("https://www.adhdstockholm.se/", "ADHD Stockholm", ""),
    ("https://www.adhdirland.ie/", "ADHD Ireland", ""),
    ("https://www.adhdfoundation.org.uk/", "ADHD Foundation UK", ""),
    ("https://www.adhdeurope.eu/contact", "ADHD Europe Contact", ""),
    ("https://www.add.org/", "ADDA", ""),
    ("https://add.org/", "ADDA alt", ""),
    ("https://www.additudemag.com/adhd-newsletter/", "ADDitude Newsletter", ""),
    ("https://www.healthline.com/health/adhd", "Healthline ADHD", ""),
    ("https://www.verywellmind.com/adhd-4157219", "Verywell Mind ADHD", ""),
    ("https://www.psychologytoday.com/us/basics/adhd", "Psychology Today ADHD", ""),
    ("https://www.webmd.com/add-adhd/default.htm", "WebMD ADHD", ""),
    ("https://www.mayoclinic.org/diseases-conditions/adhd/symptoms-causes/syc-20350889", "Mayo ADHD", ""),
    ("https://www.nimh.nih.gov/health/topics/attention-deficit-hyperactivity-disorder-adhd", "NIMH ADHD", ""),
    ("https://www.cdc.gov/ncbddd/adhd/index.html", "CDC ADHD", ""),
]

YOUTUBE_SEEDS = [
    ("https://www.howtoadhd.com/", "How to ADHD", "Jessica McCabe"),
    ("https://www.youtube.com/@HowtoADHD", "How to ADHD YT", "Jessica McCabe"),
    ("https://www.thomasfrank.com/", "Thomas Frank", ""),
    ("https://www.aliabdaal.com/", "Ali Abdaal", ""),
    ("https://www.ruriohama.com/", "Ruri Ohama", ""),
    ("https://www.augustbradley.com/", "August Bradley", ""),
    ("https://www.redgregory.com/", "Red Gregory", ""),
    ("https://www.keepproductive.com/", "Keep Productive", ""),
    ("https://www.notionmastery.com/", "Notion Mastery", ""),
    ("https://www.mariepoulin.com/", "Marie Poulin", ""),
    ("https://www.carlpullein.com/", "Carl Pullein", ""),
    ("https://www.productivitygame.com/", "Productivity Game", ""),
    ("https://www.asianefficiency.com/", "Asian Efficiency", ""),
    ("https://www.ihasadhd.com/", "I Have ADHD", "Kristen Carder"),
    ("https://www.kristencarder.com/", "Kristen Carder", ""),
    ("https://www.adhdrewired.com/", "ADHD reWired", ""),
    ("https://www.hackingyouradhd.com/", "Hacking Your ADHD", ""),
    ("https://www.adhdessentials.com/", "ADHD Essentials", ""),
    ("https://shankman.com/", "Peter Shankman", ""),
    ("https://www.fasterthanormal.com/", "Faster Than Normal", ""),
    ("https://www.adhdrollercoaster.org/", "ADHD Roller Coaster", ""),
    ("https://www.drhallowell.com/", "Dr Hallowell", ""),
    ("https://www.beyondbooksmart.com/", "Beyond BookSmart", ""),
    ("https://www.impactparents.com/", "Impact Parents", ""),
    ("https://www.takecontroladhd.com/", "Take Control ADHD", ""),
    ("https://www.adhdfriendlylifestyle.com/", "ADHD Friendly Lifestyle", ""),
    ("https://www.focusedadult.com/", "Focused Adult", ""),
    ("https://www.myndforadhd.com/", "Mynd", ""),
    ("https://www.adhdvision.com/", "ADHD Vision", ""),
    ("https://www.theadhdacademy.com/", "The ADHD Academy", ""),
    ("https://www.authenticadhd.com/", "Authentic ADHD", ""),
    ("https://www.adhdlove.com/", "ADHD Love", ""),
    ("https://www.adhddiversified.com/", "ADHD Diversified", ""),
    ("https://www.learntotalkadhd.com/", "Learn to Talk ADHD", ""),
    ("https://www.adultingwithadhd.com/", "Adulting with ADHD", ""),
    ("https://www.adhdthriveinstitute.com/", "ADHD Thrive Institute", ""),
    ("https://www.thriveadhdcoach.co.uk/", "Thrive ADHD Coach", ""),
    ("https://www.adhd2bb.com/", "ADHD 2.0 Beyond", ""),
    ("https://www.neurodivergentpodcast.com/", "Neurodivergent Podcast", ""),
    ("https://www.thesystemsmadebetter.com/", "Systems Made Better", ""),
    ("https://www.getorganizedhq.com/", "Get Organized HQ", ""),
    ("https://www.productivityist.com/", "Productivityist", ""),
    ("https://www.beyondtheto-do.com/", "Beyond the To-Do List", ""),
    ("https://www.fortelabs.com/", "Forte Labs", ""),
    ("https://www.buildingasecondbrain.com/", "BASB", ""),
    ("https://zenhabits.net/", "Zen Habits", ""),
    ("https://www.calnewport.com/", "Cal Newport", ""),
    ("https://jamesclear.com/", "James Clear", ""),
    ("https://www.thesweetsetup.com/", "The Sweet Setup", ""),
    ("https://every.to/", "Every", ""),
    ("https://www.focusmate.com/", "Focusmate", ""),
    ("https://www.inflowapp.com/", "Inflow", ""),
    ("https://www.gosimmer.com/", "Shimmer", ""),
    ("https://www.tiimoapp.com/", "Tiimo", ""),
    ("https://goblin.tools/", "Goblin Tools", ""),
    ("https://www.sunsama.com/", "Sunsama", ""),
    ("https://www.usemotion.com/", "Motion", ""),
    ("https://obsidian.md/", "Obsidian", ""),
    ("https://www.readwise.io/", "Readwise", ""),
    ("https://www.todoist.com/", "Todoist", ""),
    ("https://ticktick.com/", "TickTick", ""),
    ("https://www.notion.vip/", "Notion VIP", ""),
    ("https://easlo.co/", "Easlo", ""),
    ("https://www.productivedude.com/", "Productive Dude", ""),
    ("https://www.notionforbusiness.com/", "Notion for Business", ""),
    ("https://www.notioneverything.com/", "Notion Everything", ""),
    ("https://www.notionlife.com/", "Notion Life", ""),
    ("https://www.template.club/", "Template Club", ""),
    ("https://www.super.so/", "Super", ""),
    ("https://www.simple.ink/", "Simple.ink", ""),
    ("https://www.noteforms.com/", "NoteForms", ""),
    ("https://www.indify.co/", "Indify", ""),
    ("https://www.widgetbox.app/", "WidgetBox", ""),
    ("https://www.apothem.io/", "Apothem", ""),
    ("https://www.notionapps.com/", "Notion Apps", ""),
    ("https://www.automate.io/", "Automate.io", ""),
    ("https://www.relume.io/", "Relume", ""),
    ("https://www.framer.com/", "Framer", ""),
    ("https://www.webflow.com/", "Webflow", ""),
    ("https://www.carrd.co/", "Carrd", ""),
    ("https://www.stan.store/", "Stan Store", ""),
    ("https://www.beacons.ai/", "Beacons", ""),
    ("https://www.linktr.ee/", "Linktree", ""),
    ("https://www.kit.com/", "Kit", ""),
    ("https://convertkit.com/", "ConvertKit", ""),
    ("https://www.beehiiv.com/", "Beehiiv", ""),
    ("https://www.ghost.org/", "Ghost", ""),
    ("https://www.medium.com/", "Medium", ""),
    ("https://hashnode.com/", "Hashnode", ""),
    ("https://www.skool.com/", "Skool", ""),
    ("https://www.circle.so/", "Circle", ""),
    ("https://www.discord.com/", "Discord", ""),
    ("https://www.patreon.com/", "Patreon", ""),
    ("https://www.kofi.com/", "Ko-fi", ""),
    ("https://www.buymeacoffee.com/", "Buy Me a Coffee", ""),
    ("https://www.lemonsqueezy.com/", "Lemon Squeezy", ""),
    ("https://www.paddle.com/", "Paddle", ""),
    ("https://www.teachable.com/", "Teachable", ""),
    ("https://www.thinkific.com/", "Thinkific", ""),
    ("https://www.kajabi.com/", "Kajabi", ""),
    ("https://www.podia.com/", "Podia", ""),
    ("https://www.skillshare.com/", "Skillshare", ""),
    ("https://www.udemy.com/", "Udemy", ""),
    ("https://www.coursera.org/", "Coursera", ""),
    ("https://www.masterclass.com/", "MasterClass", ""),
]


def log(msg: str) -> None:
    print(msg, flush=True)


def fetch(url: str, timeout: int = 18) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except Exception:
        return ""


def norm_email(email: str) -> str:
    return (email or "").strip().lower()


def norm_url(url: str) -> str:
    u = (url or "").strip().lower().rstrip("/")
    return re.sub(r"^mailto:", "", u)


def is_valid_email(email: str) -> bool:
    e = norm_email(email)
    if not e or e in SKIP_EMAILS:
        return False
    if not EMAIL_RE.fullmatch(e):
        return False
    domain = e.split("@", 1)[1]
    if domain in SKIP_EMAIL_DOMAINS:
        return False
    if any(x in e for x in (
        "example.com", "sentry.io", "w3.org", "schema.org", "wixpress.com",
        "cloudfront", "png", "jpg", "jpeg", "gif", "svg", "webp",
        "2x.", "3x.", "@2x", "noreply", "no-reply", "donotreply",
    )):
        return False
    local, _, dom = e.partition("@")
    if len(local) < 2 or "." not in dom:
        return False
    parts = dom.split(".")
    if any(len(p) < 2 for p in parts):
        return False
    # reject image/file-looking locals
    if re.search(r"\.(png|jpg|jpeg|gif|svg|webp|css|js)$", local):
        return False
    return True


def extract_emails(text: str) -> list[str]:
    found: list[str] = []
    for raw in EMAIL_RE.findall(text or ""):
        raw = unescape(raw).strip().rstrip(".,;:")
        if is_valid_email(raw):
            found.append(raw)
    for m in re.finditer(r"mailto:([^\"'\s>?]+)", text or "", re.I):
        raw = unescape(m.group(1)).split("?")[0].strip()
        if is_valid_email(raw):
            found.append(raw)
    # obfuscated: name [at] domain [dot] com
    for m in re.finditer(
        r"([a-zA-Z0-9._%+\-]+)\s*(?:\[at\]|\(at\)|\sat\s)\s*([a-zA-Z0-9.\-]+)\s*(?:\[dot\]|\(dot\)|\sdot\s)\s*([a-zA-Z]{2,})",
        text or "",
        re.I,
    ):
        raw = f"{m.group(1)}@{m.group(2)}.{m.group(3)}"
        if is_valid_email(raw):
            found.append(raw)
    return list(dict.fromkeys(found))


def load_existing() -> tuple[set[str], set[str]]:
    emails: set[str] = set()
    urls: set[str] = set()

    def absorb(path: Path) -> None:
        if not path.exists():
            return
        try:
            data = json.loads(path.read_text())
        except Exception:
            return
        items = data if isinstance(data, list) else data.get("sent", []) + data.get("skipped", [])
        for c in items:
            if not isinstance(c, dict):
                continue
            e = norm_email(c.get("contact_email") or c.get("email", ""))
            if e:
                emails.add(e)
            for key in ("profile_url", "contact_url", "youtube_url"):
                u = norm_url(c.get(key, ""))
                if u and not u.startswith("mailto:"):
                    urls.add(u)

    absorb(MASTER)
    absorb(SEND_LOG)
    for batch in MARKETING.glob("_batch*.json"):
        if batch.resolve() == OUT.resolve():
            continue
        absorb(batch)
    # also absorb creator list
    absorb(MARKETING / "creator-outreach-list.json")
    return emails, urls


def notion_next_data(html: str) -> dict | None:
    m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html, re.DOTALL)
    if not m:
        return None
    try:
        return json.loads(m.group(1))
    except json.JSONDecodeError:
        return None


def notion_profile_email(username: str) -> str | None:
    html = fetch(f"https://www.notion.com/@{username}")
    data = notion_next_data(html)
    if data:
        prof = data.get("props", {}).get("pageProps", {}).get("marketplaceProfile", {})
        email = (prof.get("attributes") or {}).get("contact_email")
        if email and is_valid_email(email):
            return email
    emails = extract_emails(html)
    return emails[0] if emails else None


def make_entry(
    *,
    channel_name: str,
    contact_name: str,
    platform: str,
    profile_url: str,
    audience: int,
    niche: str,
    email: str,
    priority: str,
    notes: str,
) -> dict:
    return {
        "channel_name": channel_name[:200],
        "contact_name": contact_name,
        "platform": platform,
        "profile_url": profile_url,
        "subscribers_or_audience": audience,
        "niche_focus": niche,
        "contact_email": email,
        "contact_type": "email",
        "contact_url": f"mailto:{email}",
        "sells_digital_products": "yes",
        "outreach_priority": priority,
        "notes": notes,
        "research_ring": RESEARCH_RING,
        "in_target_range": True,
    }


def scrape_notion_categories(
    existing_emails: set[str],
    existing_urls: set[str],
    seen_emails: set[str],
    seen_urls: set[str],
    limit: int,
) -> list[dict]:
    results: list[dict] = []
    pending_profiles: dict[str, dict] = {}

    def fetch_category_page(cat_page: tuple[str, int]) -> list[dict]:
        cat, page = cat_page
        html = fetch(f"https://www.notion.com/templates/category/{cat}?page={page}")
        data = notion_next_data(html)
        if not data:
            return []
        return data.get("props", {}).get("pageProps", {}).get("templates", []) or []

    def fetch_search(query: str) -> list[dict]:
        html = fetch(f"https://www.notion.com/templates/search?query={quote(query)}")
        data = notion_next_data(html)
        if not data:
            return []
        props = data.get("props", {}).get("pageProps", {})
        return props.get("templates", []) or props.get("results", []) or []

    # deeper pagination than ring 7 (pages 1–30)
    jobs = [(cat, page) for cat in NOTION_CATEGORIES for page in range(1, 31)]
    log(f"  fetching {len(jobs)} Notion category pages + {len(NOTION_SEARCH_QUERIES)} searches...")

    creators_found: dict[str, dict] = {}

    def absorb_templates(templates: list, source: str) -> None:
        for t in templates:
            if not isinstance(t, dict):
                continue
            prof = t.get("profile") or t.get("creator") or {}
            if not isinstance(prof, dict):
                continue
            username = (prof.get("username") or "").strip()
            if not username or username.lower() == "notion":
                continue
            profile_url = f"https://www.notion.com/@{username}"
            purl = norm_url(profile_url)
            if purl in existing_urls or purl in seen_urls or username in creators_found:
                continue
            email = (prof.get("attributes") or {}).get("contact_email", "") or prof.get("email", "")
            creators_found[username] = {
                "name": prof.get("name") or username,
                "email": email,
                "profile_url": profile_url,
                "source": source,
            }

    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        futures = {pool.submit(fetch_category_page, j): ("cat", j) for j in jobs}
        futures.update({pool.submit(fetch_search, q): ("search", q) for q in NOTION_SEARCH_QUERIES})
        done = 0
        total = len(futures)
        for fut in as_completed(futures):
            done += 1
            if done % 80 == 0:
                log(f"    ...{done}/{total} Notion list pages | creators so far {len(creators_found)}")
            kind, meta = futures[fut]
            try:
                templates = fut.result()
            except Exception:
                continue
            source = f"category={meta[0]}" if kind == "cat" else f"search={meta}"
            absorb_templates(templates, source)

    log(f"  unique new Notion creators from listings: {len(creators_found)}")

    for username, info in creators_found.items():
        if len(results) >= limit:
            break
        email = info.get("email") or ""
        if not email or not is_valid_email(email):
            pending_profiles[username] = info
            continue
        em = norm_email(email)
        if em in existing_emails or em in seen_emails:
            continue
        entry = make_entry(
            channel_name=info["name"],
            contact_name="",
            platform="other",
            profile_url=info["profile_url"],
            audience=8000,
            niche="Notion templates, productivity/PKM",
            email=email,
            priority="medium",
            notes=f"Notion marketplace (@{username}), {info['source']}. Email on listing. Ring 8.",
        )
        results.append(entry)
        seen_emails.add(em)
        seen_urls.add(norm_url(info["profile_url"]))

    log(f"  inline emails: {len(results)} | profile fetch needed: {len(pending_profiles)}")

    if len(results) < limit and pending_profiles:
        # fetch many profiles — multiplier high to hit yield
        need = min(len(pending_profiles), max((limit - len(results)) * 4, 800))
        to_fetch = list(pending_profiles.items())[:need]
        log(f"  fetching {len(to_fetch)} Notion profile pages...")

        with ThreadPoolExecutor(max_workers=WORKERS) as pool:
            futs = {pool.submit(notion_profile_email, u): (u, info) for u, info in to_fetch}
            done = 0
            for fut in as_completed(futs):
                done += 1
                if done % 100 == 0:
                    log(f"    ...profiles {done}/{len(to_fetch)} | emails {len(results)}")
                if len(results) >= limit:
                    break
                username, info = futs[fut]
                try:
                    email = fut.result()
                except Exception:
                    continue
                if not email or not is_valid_email(email):
                    continue
                em = norm_email(email)
                if em in existing_emails or em in seen_emails:
                    continue
                entry = make_entry(
                    channel_name=info["name"],
                    contact_name="",
                    platform="other",
                    profile_url=info["profile_url"],
                    audience=8000,
                    niche="Notion templates, productivity/PKM",
                    email=email,
                    priority="medium",
                    notes=f"Notion marketplace (@{username}), {info['source']}. Email on profile. Ring 8.",
                )
                results.append(entry)
                seen_emails.add(em)
                seen_urls.add(norm_url(info["profile_url"]))

    return results


def scrape_gumroad(
    existing_emails: set[str],
    existing_urls: set[str],
    seen_emails: set[str],
    seen_urls: set[str],
    limit: int,
) -> list[dict]:
    results: list[dict] = []
    sellers: dict[str, str] = {}

    def fetch_discover(query: str) -> None:
        html = fetch(f"https://gumroad.com/discover?query={quote(query)}")
        for seller, _product in re.findall(
            r"https://([a-zA-Z0-9_-]+)\.gumroad\.com/l/([a-zA-Z0-9_-]+)", html
        ):
            if seller in ("assets", "app", "help", "blog", "status", "discover"):
                continue
            sellers.setdefault(seller, query)
        # also /username patterns
        for seller in re.findall(r"gumroad\.com/([a-zA-Z0-9_-]{2,40})(?:\"|'|/|\?)", html):
            if seller in ("discover", "l", "features", "pricing", "about", "login", "signup", "d"):
                continue
            sellers.setdefault(seller, query)

    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        list(pool.map(fetch_discover, GUMROAD_QUERIES))

    log(f"  Gumroad sellers discovered: {len(sellers)}")

    def process_seller(item: tuple[str, str]) -> dict | None:
        seller, query = item
        profile_url = f"https://{seller}.gumroad.com/"
        purl = norm_url(profile_url)
        if purl in existing_urls or purl in seen_urls:
            return None

        html = fetch(profile_url)
        if not html:
            html = fetch(f"https://gumroad.com/{seller}")
        emails = extract_emails(html)
        product_links = re.findall(
            rf"https://{re.escape(seller)}\.gumroad\.com/l/([a-zA-Z0-9_-]+)", html
        )
        for plink in product_links[:3]:
            emails.extend(extract_emails(fetch(f"https://{seller}.gumroad.com/l/{plink}")))

        ext_links = re.findall(r'href="(https?://[^"]+)"', html)
        for link in ext_links[:5]:
            host = urlparse(link).netloc.lower()
            if any(x in host for x in (
                "gumroad", "twitter", "x.com", "instagram", "youtube", "facebook",
                "tiktok", "linkedin", "pinterest", "threads", "reddit",
            )):
                continue
            emails.extend(extract_emails(fetch(link)))

        emails = list(dict.fromkeys(emails))
        if not emails:
            return None
        email = emails[0]
        em = norm_email(email)
        if em in existing_emails or em in seen_emails:
            return None

        niche = "Digital templates/productivity (Gumroad)"
        q = query.lower()
        if "adhd" in q or "adhd" in seller.lower() or "neuro" in q:
            niche = "ADHD planners/templates on Gumroad"
            priority = "high"
        elif "notion" in q or "notion" in seller.lower():
            niche = "Notion templates on Gumroad"
            priority = "medium"
        else:
            priority = "medium"

        return make_entry(
            channel_name=seller.replace("-", " ").replace("_", " ").title(),
            contact_name="",
            platform="other",
            profile_url=profile_url,
            audience=8000,
            niche=niche,
            email=email,
            priority=priority,
            notes=f"Gumroad seller ({seller}). Query '{query}'. Ring 8.",
        )

    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        futs = [pool.submit(process_seller, item) for item in sellers.items()]
        for fut in as_completed(futs):
            if len(results) >= limit:
                break
            try:
                entry = fut.result()
            except Exception:
                continue
            if entry:
                em = norm_email(entry["contact_email"])
                if em not in seen_emails:
                    results.append(entry)
                    seen_emails.add(em)
                    seen_urls.add(norm_url(entry["profile_url"]))

    return results


def scrape_substack(
    existing_emails: set[str],
    existing_urls: set[str],
    seen_emails: set[str],
    seen_urls: set[str],
    limit: int,
) -> list[dict]:
    results: list[dict] = []
    # unique slugs only (filter spaces)
    seeds = []
    for s in SUBSTACK_SEEDS:
        s = s.strip().lower().replace(" ", "")
        if s and s not in seeds and re.fullmatch(r"[a-z0-9_-]+", s):
            seeds.append(s)

    def process_slug(slug: str) -> dict | None:
        profile_url = f"https://{slug}.substack.com/"
        purl = norm_url(profile_url)
        if purl in existing_urls or purl in seen_urls:
            return None
        html = fetch(f"https://{slug}.substack.com/about") or fetch(profile_url)
        if not html or "Publication not found" in html or "There's nothing here" in html:
            return None
        emails = extract_emails(html)
        if not emails:
            return None
        email = emails[0]
        em = norm_email(email)
        if em in existing_emails or em in seen_emails:
            return None
        title_m = re.search(r"<title>([^<]+)</title>", html, re.I)
        title = slug.replace("-", " ").title()
        if title_m:
            title = re.sub(r"\s*[\|·].*$", "", title_m.group(1)).strip() or title
        return make_entry(
            channel_name=title,
            contact_name="",
            platform="newsletter",
            profile_url=profile_url,
            audience=12000,
            niche="ADHD/productivity/neurodivergent newsletter",
            email=email,
            priority="high",
            notes=f"Substack (@{slug}). Ring 8.",
        )

    log(f"  checking {len(seeds)} Substack slugs...")
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        futs = {pool.submit(process_slug, s): s for s in seeds}
        for fut in as_completed(futs):
            if len(results) >= limit:
                break
            try:
                entry = fut.result()
            except Exception:
                continue
            if entry:
                em = norm_email(entry["contact_email"])
                if em not in seen_emails:
                    results.append(entry)
                    seen_emails.add(em)
                    seen_urls.add(norm_url(entry["profile_url"]))

    return results


def scrape_beehiiv(
    existing_emails: set[str],
    existing_urls: set[str],
    seen_emails: set[str],
    seen_urls: set[str],
    limit: int,
) -> list[dict]:
    """Discover beehiiv pubs via search pages and extract emails from about."""
    results: list[dict] = []
    pubs: set[str] = set()

    def discover(q: str) -> None:
        html = fetch(f"https://www.beehiiv.com/search?query={quote(q)}")
        for m in re.findall(r"https?://([a-zA-Z0-9-]+)\.beehiiv\.com", html):
            if m not in ("www", "app", "support", "blog", "help"):
                pubs.add(m)
        for m in re.findall(r"beehiiv\.com/p/([a-zA-Z0-9-]+)", html):
            pubs.add(m)

    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        list(pool.map(discover, BEEHIIV_SEEDS))

    log(f"  Beehiiv pubs discovered: {len(pubs)}")

    def process_pub(slug: str) -> dict | None:
        profile_url = f"https://{slug}.beehiiv.com/"
        purl = norm_url(profile_url)
        if purl in existing_urls or purl in seen_urls:
            return None
        html = fetch(profile_url) or fetch(f"https://{slug}.beehiiv.com/about")
        emails = extract_emails(html)
        if not emails:
            return None
        email = emails[0]
        em = norm_email(email)
        if em in existing_emails or em in seen_emails:
            return None
        return make_entry(
            channel_name=slug.replace("-", " ").title(),
            contact_name="",
            platform="newsletter",
            profile_url=profile_url,
            audience=10000,
            niche="Newsletter (Beehiiv) — productivity/ADHD-adjacent",
            email=email,
            priority="medium",
            notes=f"Beehiiv ({slug}). Ring 8.",
        )

    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        futs = [pool.submit(process_pub, s) for s in pubs]
        for fut in as_completed(futs):
            if len(results) >= limit:
                break
            try:
                entry = fut.result()
            except Exception:
                continue
            if entry:
                em = norm_email(entry["contact_email"])
                if em not in seen_emails:
                    results.append(entry)
                    seen_emails.add(em)
                    seen_urls.add(norm_url(entry["profile_url"]))

    return results


def scrape_site_seeds(
    seeds: list[tuple[str, str, str]],
    platform: str,
    niche: str,
    existing_emails: set[str],
    existing_urls: set[str],
    seen_emails: set[str],
    seen_urls: set[str],
    limit: int,
) -> list[dict]:
    results: list[dict] = []
    contact_paths = [
        "", "/contact", "/contact-us", "/about", "/about-us", "/work-with-me",
        "/collaborate", "/media", "/press", "/partnerships", "/sponsors",
        "/advertise", "/business", "/coaching", "/services", "/connect",
    ]

    def process_seed(seed: tuple[str, str, str]) -> dict | None:
        site_url, name, contact_name = seed
        parsed = urlparse(site_url)
        if not parsed.scheme:
            return None
        base = f"{parsed.scheme}://{parsed.netloc}"
        purl = norm_url(site_url)
        if purl in existing_urls or purl in seen_urls:
            # still try if we never got email for this domain
            pass
        emails: list[str] = []
        for path in contact_paths:
            emails.extend(extract_emails(fetch(urljoin(base, path))))
            if emails:
                break
        emails = list(dict.fromkeys(emails))
        if not emails:
            return None
        preferred = None
        for e in emails:
            local = e.split("@")[0].lower()
            if local in (
                "hello", "contact", "business", "media", "partnerships", "collab",
                "info", "mgmt", "press", "partners", "sponsor", "affiliates",
            ):
                preferred = e
                break
        email = preferred or emails[0]
        em = norm_email(email)
        if em in existing_emails or em in seen_emails:
            return None
        priority = "high" if platform in ("podcast", "youtube") else "medium"
        return make_entry(
            channel_name=name,
            contact_name=contact_name,
            platform=platform,
            profile_url=site_url,
            audience=15000 if platform == "youtube" else 10000,
            niche=niche,
            email=email,
            priority=priority,
            notes=f"{platform.title()} site. Business email on contact/about. Ring 8.",
        )

    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        futs = {pool.submit(process_seed, s): s for s in seeds}
        for fut in as_completed(futs):
            if len(results) >= limit:
                break
            try:
                entry = fut.result()
            except Exception:
                continue
            if entry:
                em = norm_email(entry["contact_email"])
                if em not in seen_emails:
                    results.append(entry)
                    seen_emails.add(em)
                    seen_urls.add(norm_url(entry["profile_url"]))

    return results


def run(limit: int = 1000, dry_run: bool = False) -> dict:
    existing_emails, existing_urls = load_existing()
    seen_emails: set[str] = set()
    seen_urls: set[str] = set()
    all_results: list[dict] = []

    log(f"Existing: {len(existing_emails)} emails, {len(existing_urls)} profile URLs")
    log(f"Target: {limit} new contacts (Ring {RESEARCH_RING})")

    phases = [
        ("Notion Marketplace (deep)", lambda rem: scrape_notion_categories(
            existing_emails, existing_urls, seen_emails, seen_urls, rem)),
        ("Gumroad Discover", lambda rem: scrape_gumroad(
            existing_emails, existing_urls, seen_emails, seen_urls, rem)),
        ("Substack newsletters", lambda rem: scrape_substack(
            existing_emails, existing_urls, seen_emails, seen_urls, rem)),
        ("Beehiiv newsletters", lambda rem: scrape_beehiiv(
            existing_emails, existing_urls, seen_emails, seen_urls, rem)),
        ("ADHD/productivity sites & podcasts", lambda rem: scrape_site_seeds(
            PODCAST_SEEDS, "podcast", "ADHD/productivity podcast/site",
            existing_emails, existing_urls, seen_emails, seen_urls, rem)),
        ("YouTube/creator sites", lambda rem: scrape_site_seeds(
            YOUTUBE_SEEDS, "youtube", "ADHD/Notion/productivity creator",
            existing_emails, existing_urls, seen_emails, seen_urls, rem)),
    ]

    t0 = time.time()
    for phase_name, fn in phases:
        remaining = limit - len(all_results)
        if remaining <= 0:
            break
        log(f"\n==> {phase_name} (need {remaining})")
        batch = fn(remaining)
        log(f"    +{len(batch)} new contacts (running total {len(all_results) + len(batch)})")
        all_results.extend(batch)

    deduped: list[dict] = []
    batch_seen: set[str] = set()
    for c in all_results:
        key = norm_email(c["contact_email"])
        if key in batch_seen or key in existing_emails:
            continue
        batch_seen.add(key)
        deduped.append(c)
    deduped = deduped[:limit]

    stats = {
        "saved": len(deduped),
        "target": limit,
        "elapsed_sec": round(time.time() - t0, 1),
        "existing_emails_before": len(existing_emails),
        "by_platform": {},
        "by_priority": {},
    }
    for c in deduped:
        p = c["platform"]
        stats["by_platform"][p] = stats["by_platform"].get(p, 0) + 1
        pr = c["outreach_priority"]
        stats["by_priority"][pr] = stats["by_priority"].get(pr, 0) + 1

    if not dry_run:
        OUT.write_text(json.dumps(deduped, indent=2) + "\n")
        log(f"\nWrote {len(deduped)} contacts to {OUT}")
    else:
        log(f"\nDry run — would save {len(deduped)} contacts")

    return {"contacts": deduped, "stats": stats}


def main() -> None:
    parser = argparse.ArgumentParser(description="Ring 8 affiliate outreach research")
    parser.add_argument("--limit", type=int, default=1000, help="Max new contacts to save")
    parser.add_argument("--dry-run", action="store_true", help="Stats only, no file write")
    args = parser.parse_args()
    result = run(limit=args.limit, dry_run=args.dry_run)
    log(json.dumps(result["stats"], indent=2))


if __name__ == "__main__":
    main()
