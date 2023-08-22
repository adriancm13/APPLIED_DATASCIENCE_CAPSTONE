{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "<p style=\"text-align:center\">\n",
    "    <a href=\"https://skills.network/?utm_medium=Exinfluencer&utm_source=Exinfluencer&utm_content=000026UJ&utm_term=10006555&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMDS0321ENSkillsNetwork865-2023-01-01\">\n",
    "    <img src=\"https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/assets/logos/SN_web_lightmode.png\" width=\"200\" alt=\"Skills Network Logo\"  />\n",
    "    </a>\n",
    "</p>\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# **Space X  Falcon 9 First Stage Landing Prediction**\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Web scraping Falcon 9 and Falcon Heavy Launches Records from Wikipedia\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Estimated time needed: **40** minutes\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "In this lab, you will be performing web scraping to collect Falcon 9 historical launch records from a Wikipedia page titled `List of Falcon 9 and Falcon Heavy launches`\n",
    "\n",
    "https://en.wikipedia.org/wiki/List_of_Falcon_9_and_Falcon_Heavy_launches\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "![](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_1_L2/images/Falcon9_rocket_family.svg)\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Falcon 9 first stage will land successfully\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "![](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DS0701EN-SkillsNetwork/api/Images/landing_1.gif)\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Several examples of an unsuccessful landing are shown here:\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "![](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DS0701EN-SkillsNetwork/api/Images/crash.gif)\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "More specifically, the launch records are stored in a HTML table shown below:\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "![](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_1_L2/images/falcon9-launches-wiki.png)\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "  ## Objectives\n",
    "Web scrap Falcon 9 launch records with `BeautifulSoup`: \n",
    "- Extract a Falcon 9 launch records HTML table from Wikipedia\n",
    "- Parse the table and convert it into a Pandas data frame\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "First let's import required packages for this lab\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Requirement already satisfied: beautifulsoup4 in /home/jupyterlab/conda/envs/python/lib/python3.7/site-packages (4.11.1)\n",
      "Requirement already satisfied: soupsieve>1.2 in /home/jupyterlab/conda/envs/python/lib/python3.7/site-packages (from beautifulsoup4) (2.3.2.post1)\n",
      "Requirement already satisfied: requests in /home/jupyterlab/conda/envs/python/lib/python3.7/site-packages (2.29.0)\n",
      "Requirement already satisfied: charset-normalizer<4,>=2 in /home/jupyterlab/conda/envs/python/lib/python3.7/site-packages (from requests) (3.1.0)\n",
      "Requirement already satisfied: idna<4,>=2.5 in /home/jupyterlab/conda/envs/python/lib/python3.7/site-packages (from requests) (3.4)\n",
      "Requirement already satisfied: urllib3<1.27,>=1.21.1 in /home/jupyterlab/conda/envs/python/lib/python3.7/site-packages (from requests) (1.26.15)\n",
      "Requirement already satisfied: certifi>=2017.4.17 in /home/jupyterlab/conda/envs/python/lib/python3.7/site-packages (from requests) (2023.5.7)\n"
     ]
    }
   ],
   "source": [
    "!pip3 install beautifulsoup4\n",
    "!pip3 install requests"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {
    "tags": []
   },
   "outputs": [],
   "source": [
    "import sys\n",
    "\n",
    "import requests\n",
    "from bs4 import BeautifulSoup\n",
    "import re\n",
    "import unicodedata\n",
    "import pandas as pd"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "and we will provide some helper functions for you to process web scraped HTML table\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {
    "tags": []
   },
   "outputs": [],
   "source": [
    "def date_time(table_cells):\n",
    "    \"\"\"\n",
    "    This function returns the data and time from the HTML  table cell\n",
    "    Input: the  element of a table data cell extracts extra row\n",
    "    \"\"\"\n",
    "    return [data_time.strip() for data_time in list(table_cells.strings)][0:2]\n",
    "\n",
    "def booster_version(table_cells):\n",
    "    \"\"\"\n",
    "    This function returns the booster version from the HTML  table cell \n",
    "    Input: the  element of a table data cell extracts extra row\n",
    "    \"\"\"\n",
    "    out=''.join([booster_version for i,booster_version in enumerate( table_cells.strings) if i%2==0][0:-1])\n",
    "    return out\n",
    "\n",
    "def landing_status(table_cells):\n",
    "    \"\"\"\n",
    "    This function returns the landing status from the HTML table cell \n",
    "    Input: the  element of a table data cell extracts extra row\n",
    "    \"\"\"\n",
    "    out=[i for i in table_cells.strings][0]\n",
    "    return out\n",
    "\n",
    "\n",
    "def get_mass(table_cells):\n",
    "    mass=unicodedata.normalize(\"NFKD\", table_cells.text).strip()\n",
    "    if mass:\n",
    "        mass.find(\"kg\")\n",
    "        new_mass=mass[0:mass.find(\"kg\")+2]\n",
    "    else:\n",
    "        new_mass=0\n",
    "    return new_mass\n",
    "\n",
    "\n",
    "def extract_column_from_header(row):\n",
    "    \"\"\"\n",
    "    This function returns the landing status from the HTML table cell \n",
    "    Input: the  element of a table data cell extracts extra row\n",
    "    \"\"\"\n",
    "    if (row.br):\n",
    "        row.br.extract()\n",
    "    if row.a:\n",
    "        row.a.extract()\n",
    "    if row.sup:\n",
    "        row.sup.extract()\n",
    "        \n",
    "    colunm_name = ' '.join(row.contents)\n",
    "    \n",
    "    # Filter the digit and empty names\n",
    "    if not(colunm_name.strip().isdigit()):\n",
    "        colunm_name = colunm_name.strip()\n",
    "        return colunm_name    \n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "To keep the lab tasks consistent, you will be asked to scrape the data from a snapshot of the  `List of Falcon 9 and Falcon Heavy launches` Wikipage updated on\n",
    "`9th June 2021`\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {
    "tags": []
   },
   "outputs": [],
   "source": [
    "static_url = \"https://en.wikipedia.org/w/index.php?title=List_of_Falcon_9_and_Falcon_Heavy_launches&oldid=1027686922\""
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Next, request the HTML page from the above URL and get a `response` object\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### TASK 1: Request the Falcon9 Launch Wiki page from its URL\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "First, let's perform an HTTP GET method to request the Falcon9 Launch HTML page, as an HTTP response.\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "200"
      ]
     },
     "execution_count": 8,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# use requests.get() method with the provided static_url\n",
    "# assign the response to a object\n",
    "html_data= requests.get(static_url)\n",
    "html_data.status_code"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Create a `BeautifulSoup` object from the HTML `response`\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "metadata": {
    "tags": []
   },
   "outputs": [],
   "source": [
    "# Use BeautifulSoup() to create a BeautifulSoup object from a response text content\n",
    "soup = BeautifulSoup(html_data.text)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Print the page title to verify if the `BeautifulSoup` object was created properly \n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "<title>List of Falcon 9 and Falcon Heavy launches - Wikipedia</title>"
      ]
     },
     "execution_count": 11,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Use soup.title attribute\n",
    "soup.title"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### TASK 2: Extract all column/variable names from the HTML table header\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Next, we want to collect all relevant column names from the HTML table header\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Let's try to find all tables on the wiki page first. If you need to refresh your memory about `BeautifulSoup`, please check the external reference link towards the end of this lab\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "metadata": {
    "tags": []
   },
   "outputs": [],
   "source": [
    "# Use the find_all function in the BeautifulSoup object, with element type `table`\n",
    "# Assign the result to a list called `html_tables`\n",
    "html_tables = soup.find_all('table')"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Starting from the third table is our target table contains the actual launch records.\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 14,
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "<table class=\"wikitable plainrowheaders collapsible\" style=\"width: 100%;\">\n",
      "<tbody><tr>\n",
      "<th scope=\"col\">Flight No.\n",
      "</th>\n",
      "<th scope=\"col\">Date and<br/>time (<a href=\"/wiki/Coordinated_Universal_Time\" title=\"Coordinated Universal Time\">UTC</a>)\n",
      "</th>\n",
      "<th scope=\"col\"><a href=\"/wiki/List_of_Falcon_9_first-stage_boosters\" title=\"List of Falcon 9 first-stage boosters\">Version,<br/>Booster</a> <sup class=\"reference\" id=\"cite_ref-booster_11-0\"><a href=\"#cite_note-booster-11\">[b]</a></sup>\n",
      "</th>\n",
      "<th scope=\"col\">Launch site\n",
      "</th>\n",
      "<th scope=\"col\">Payload<sup class=\"reference\" id=\"cite_ref-Dragon_12-0\"><a href=\"#cite_note-Dragon-12\">[c]</a></sup>\n",
      "</th>\n",
      "<th scope=\"col\">Payload mass\n",
      "</th>\n",
      "<th scope=\"col\">Orbit\n",
      "</th>\n",
      "<th scope=\"col\">Customer\n",
      "</th>\n",
      "<th scope=\"col\">Launch<br/>outcome\n",
      "</th>\n",
      "<th scope=\"col\"><a href=\"/wiki/Falcon_9_first-stage_landing_tests\" title=\"Falcon 9 first-stage landing tests\">Booster<br/>landing</a>\n",
      "</th></tr>\n",
      "<tr>\n",
      "<th rowspan=\"2\" scope=\"row\" style=\"text-align:center;\">1\n",
      "</th>\n",
      "<td>4 June 2010,<br/>18:45\n",
      "</td>\n",
      "<td><a href=\"/wiki/Falcon_9_v1.0\" title=\"Falcon 9 v1.0\">F9 v1.0</a><sup class=\"reference\" id=\"cite_ref-MuskMay2012_13-0\"><a href=\"#cite_note-MuskMay2012-13\">[7]</a></sup><br/>B0003.1<sup class=\"reference\" id=\"cite_ref-block_numbers_14-0\"><a href=\"#cite_note-block_numbers-14\">[8]</a></sup>\n",
      "</td>\n",
      "<td><a href=\"/wiki/Cape_Canaveral_Space_Force_Station\" title=\"Cape Canaveral Space Force Station\">CCAFS</a>,<br/><a href=\"/wiki/Cape_Canaveral_Space_Launch_Complex_40\" title=\"Cape Canaveral Space Launch Complex 40\">SLC-40</a>\n",
      "</td>\n",
      "<td><a href=\"/wiki/Dragon_Spacecraft_Qualification_Unit\" title=\"Dragon Spacecraft Qualification Unit\">Dragon Spacecraft Qualification Unit</a>\n",
      "</td>\n",
      "<td>\n",
      "</td>\n",
      "<td><a href=\"/wiki/Low_Earth_orbit\" title=\"Low Earth orbit\">LEO</a>\n",
      "</td>\n",
      "<td><a href=\"/wiki/SpaceX\" title=\"SpaceX\">SpaceX</a>\n",
      "</td>\n",
      "<td class=\"table-success\" style=\"background: #9EFF9E; vertical-align: middle; text-align: center;\">Success\n",
      "</td>\n",
      "<td class=\"table-failure\" style=\"background: #FFC7C7; vertical-align: middle; text-align: center;\">Failure<sup class=\"reference\" id=\"cite_ref-ns20110930_15-0\"><a href=\"#cite_note-ns20110930-15\">[9]</a></sup><sup class=\"reference\" id=\"cite_ref-16\"><a href=\"#cite_note-16\">[10]</a></sup><br/><small>(parachute)</small>\n",
      "</td></tr>\n",
      "<tr>\n",
      "<td colspan=\"9\">First flight of Falcon 9 v1.0.<sup class=\"reference\" id=\"cite_ref-sfn20100604_17-0\"><a href=\"#cite_note-sfn20100604-17\">[11]</a></sup> Used a boilerplate version of Dragon capsule which was not designed to separate from the second stage.<small>(<a href=\"#First_flight_of_Falcon_9\">more details below</a>)</small> Attempted to recover the first stage by parachuting it into the ocean, but it burned up on reentry, before the parachutes even deployed.<sup class=\"reference\" id=\"cite_ref-parachute_18-0\"><a href=\"#cite_note-parachute-18\">[12]</a></sup>\n",
      "</td></tr>\n",
      "<tr>\n",
      "<th rowspan=\"2\" scope=\"row\" style=\"text-align:center;\">2\n",
      "</th>\n",
      "<td>8 December 2010,<br/>15:43<sup class=\"reference\" id=\"cite_ref-spaceflightnow_Clark_Launch_Report_19-0\"><a href=\"#cite_note-spaceflightnow_Clark_Launch_Report-19\">[13]</a></sup>\n",
      "</td>\n",
      "<td><a href=\"/wiki/Falcon_9_v1.0\" title=\"Falcon 9 v1.0\">F9 v1.0</a><sup class=\"reference\" id=\"cite_ref-MuskMay2012_13-1\"><a href=\"#cite_note-MuskMay2012-13\">[7]</a></sup><br/>B0004.1<sup class=\"reference\" id=\"cite_ref-block_numbers_14-1\"><a href=\"#cite_note-block_numbers-14\">[8]</a></sup>\n",
      "</td>\n",
      "<td><a href=\"/wiki/Cape_Canaveral_Space_Force_Station\" title=\"Cape Canaveral Space Force Station\">CCAFS</a>,<br/><a href=\"/wiki/Cape_Canaveral_Space_Launch_Complex_40\" title=\"Cape Canaveral Space Launch Complex 40\">SLC-40</a>\n",
      "</td>\n",
      "<td><a href=\"/wiki/SpaceX_Dragon\" title=\"SpaceX Dragon\">Dragon</a> <a class=\"mw-redirect\" href=\"/wiki/COTS_Demo_Flight_1\" title=\"COTS Demo Flight 1\">demo flight C1</a><br/>(Dragon C101)\n",
      "</td>\n",
      "<td>\n",
      "</td>\n",
      "<td><a href=\"/wiki/Low_Earth_orbit\" title=\"Low Earth orbit\">LEO</a> (<a href=\"/wiki/International_Space_Station\" title=\"International Space Station\">ISS</a>)\n",
      "</td>\n",
      "<td><style data-mw-deduplicate=\"TemplateStyles:r1126788409\">.mw-parser-output .plainlist ol,.mw-parser-output .plainlist ul{line-height:inherit;list-style:none;margin:0;padding:0}.mw-parser-output .plainlist ol li,.mw-parser-output .plainlist ul li{margin-bottom:0}</style><div class=\"plainlist\">\n",
      "<ul><li><a href=\"/wiki/NASA\" title=\"NASA\">NASA</a> (<a href=\"/wiki/Commercial_Orbital_Transportation_Services\" title=\"Commercial Orbital Transportation Services\">COTS</a>)</li>\n",
      "<li><a href=\"/wiki/National_Reconnaissance_Office\" title=\"National Reconnaissance Office\">NRO</a></li></ul>\n",
      "</div>\n",
      "</td>\n",
      "<td class=\"table-success\" style=\"background: #9EFF9E; vertical-align: middle; text-align: center;\">Success<sup class=\"reference\" id=\"cite_ref-ns20110930_15-1\"><a href=\"#cite_note-ns20110930-15\">[9]</a></sup>\n",
      "</td>\n",
      "<td class=\"table-failure\" style=\"background: #FFC7C7; vertical-align: middle; text-align: center;\">Failure<sup class=\"reference\" id=\"cite_ref-ns20110930_15-2\"><a href=\"#cite_note-ns20110930-15\">[9]</a></sup><sup class=\"reference\" id=\"cite_ref-20\"><a href=\"#cite_note-20\">[14]</a></sup><br/><small>(parachute)</small>\n",
      "</td></tr>\n",
      "<tr>\n",
      "<td colspan=\"9\">Maiden flight of <a class=\"mw-redirect\" href=\"/wiki/Dragon_capsule\" title=\"Dragon capsule\">Dragon capsule</a>, consisting of over 3 hours of testing thruster maneuvering and reentry.<sup class=\"reference\" id=\"cite_ref-spaceflightnow_Clark_unleashing_Dragon_21-0\"><a href=\"#cite_note-spaceflightnow_Clark_unleashing_Dragon-21\">[15]</a></sup> Attempted to recover the first stage by parachuting it into the ocean, but it disintegrated upon reentry, before the parachutes were deployed.<sup class=\"reference\" id=\"cite_ref-parachute_18-1\"><a href=\"#cite_note-parachute-18\">[12]</a></sup> <small>(<a href=\"#COTS_demo_missions\">more details below</a>)</small> It also included two <a href=\"/wiki/CubeSat\" title=\"CubeSat\">CubeSats</a>,<sup class=\"reference\" id=\"cite_ref-NRO_Taps_Boeing_for_Next_Batch_of_CubeSats_22-0\"><a href=\"#cite_note-NRO_Taps_Boeing_for_Next_Batch_of_CubeSats-22\">[16]</a></sup> and a wheel of <a href=\"/wiki/Brou%C3%A8re\" title=\"Brouère\">Brouère</a> cheese.\n",
      "</td></tr>\n",
      "<tr>\n",
      "<th rowspan=\"2\" scope=\"row\" style=\"text-align:center;\">3\n",
      "</th>\n",
      "<td>22 May 2012,<br/>07:44<sup class=\"reference\" id=\"cite_ref-BBC_new_era_23-0\"><a href=\"#cite_note-BBC_new_era-23\">[17]</a></sup>\n",
      "</td>\n",
      "<td><a href=\"/wiki/Falcon_9_v1.0\" title=\"Falcon 9 v1.0\">F9 v1.0</a><sup class=\"reference\" id=\"cite_ref-MuskMay2012_13-2\"><a href=\"#cite_note-MuskMay2012-13\">[7]</a></sup><br/>B0005.1<sup class=\"reference\" id=\"cite_ref-block_numbers_14-2\"><a href=\"#cite_note-block_numbers-14\">[8]</a></sup>\n",
      "</td>\n",
      "<td><a href=\"/wiki/Cape_Canaveral_Space_Force_Station\" title=\"Cape Canaveral Space Force Station\">CCAFS</a>,<br/><a href=\"/wiki/Cape_Canaveral_Space_Launch_Complex_40\" title=\"Cape Canaveral Space Launch Complex 40\">SLC-40</a>\n",
      "</td>\n",
      "<td><a href=\"/wiki/SpaceX_Dragon\" title=\"SpaceX Dragon\">Dragon</a> <a class=\"mw-redirect\" href=\"/wiki/Dragon_C2%2B\" title=\"Dragon C2+\">demo flight C2+</a><sup class=\"reference\" id=\"cite_ref-C2_24-0\"><a href=\"#cite_note-C2-24\">[18]</a></sup><br/>(Dragon C102)\n",
      "</td>\n",
      "<td>525 kg (1,157 lb)<sup class=\"reference\" id=\"cite_ref-25\"><a href=\"#cite_note-25\">[19]</a></sup>\n",
      "</td>\n",
      "<td><a href=\"/wiki/Low_Earth_orbit\" title=\"Low Earth orbit\">LEO</a> (<a href=\"/wiki/International_Space_Station\" title=\"International Space Station\">ISS</a>)\n",
      "</td>\n",
      "<td><a href=\"/wiki/NASA\" title=\"NASA\">NASA</a> (<a href=\"/wiki/Commercial_Orbital_Transportation_Services\" title=\"Commercial Orbital Transportation Services\">COTS</a>)\n",
      "</td>\n",
      "<td class=\"table-success\" style=\"background: #9EFF9E; vertical-align: middle; text-align: center;\">Success<sup class=\"reference\" id=\"cite_ref-26\"><a href=\"#cite_note-26\">[20]</a></sup>\n",
      "</td>\n",
      "<td class=\"table-noAttempt\" style=\"background: #EEE; vertical-align: middle; white-space: nowrap; text-align: center;\">No attempt\n",
      "</td></tr>\n",
      "<tr>\n",
      "<td colspan=\"9\">Dragon spacecraft demonstrated a series of tests before it was allowed to approach the <a href=\"/wiki/International_Space_Station\" title=\"International Space Station\">International Space Station</a>. Two days later, it became the first commercial spacecraft to board the ISS.<sup class=\"reference\" id=\"cite_ref-BBC_new_era_23-1\"><a href=\"#cite_note-BBC_new_era-23\">[17]</a></sup> <small>(<a href=\"#COTS_demo_missions\">more details below</a>)</small>\n",
      "</td></tr>\n",
      "<tr>\n",
      "<th rowspan=\"3\" scope=\"row\" style=\"text-align:center;\">4\n",
      "</th>\n",
      "<td rowspan=\"2\">8 October 2012,<br/>00:35<sup class=\"reference\" id=\"cite_ref-SFN_LLog_27-0\"><a href=\"#cite_note-SFN_LLog-27\">[21]</a></sup>\n",
      "</td>\n",
      "<td rowspan=\"2\"><a href=\"/wiki/Falcon_9_v1.0\" title=\"Falcon 9 v1.0\">F9 v1.0</a><sup class=\"reference\" id=\"cite_ref-MuskMay2012_13-3\"><a href=\"#cite_note-MuskMay2012-13\">[7]</a></sup><br/>B0006.1<sup class=\"reference\" id=\"cite_ref-block_numbers_14-3\"><a href=\"#cite_note-block_numbers-14\">[8]</a></sup>\n",
      "</td>\n",
      "<td rowspan=\"2\"><a href=\"/wiki/Cape_Canaveral_Space_Force_Station\" title=\"Cape Canaveral Space Force Station\">CCAFS</a>,<br/><a href=\"/wiki/Cape_Canaveral_Space_Launch_Complex_40\" title=\"Cape Canaveral Space Launch Complex 40\">SLC-40</a>\n",
      "</td>\n",
      "<td><a href=\"/wiki/SpaceX_CRS-1\" title=\"SpaceX CRS-1\">SpaceX CRS-1</a><sup class=\"reference\" id=\"cite_ref-sxManifest20120925_28-0\"><a href=\"#cite_note-sxManifest20120925-28\">[22]</a></sup><br/>(Dragon C103)\n",
      "</td>\n",
      "<td>4,700 kg (10,400 lb)\n",
      "</td>\n",
      "<td><a href=\"/wiki/Low_Earth_orbit\" title=\"Low Earth orbit\">LEO</a> (<a href=\"/wiki/International_Space_Station\" title=\"International Space Station\">ISS</a>)\n",
      "</td>\n",
      "<td><a href=\"/wiki/NASA\" title=\"NASA\">NASA</a> (<a href=\"/wiki/Commercial_Resupply_Services\" title=\"Commercial Resupply Services\">CRS</a>)\n",
      "</td>\n",
      "<td class=\"table-success\" style=\"background: #9EFF9E; vertical-align: middle; text-align: center;\">Success\n",
      "</td>\n",
      "<td rowspan=\"2\" style=\"background:#ececec; text-align:center;\"><span class=\"nowrap\">No attempt</span>\n",
      "</td></tr>\n",
      "<tr>\n",
      "<td><a href=\"/wiki/Orbcomm_(satellite)\" title=\"Orbcomm (satellite)\">Orbcomm-OG2</a><sup class=\"reference\" id=\"cite_ref-Orbcomm_29-0\"><a href=\"#cite_note-Orbcomm-29\">[23]</a></sup>\n",
      "</td>\n",
      "<td>172 kg (379 lb)<sup class=\"reference\" id=\"cite_ref-gunter-og2_30-0\"><a href=\"#cite_note-gunter-og2-30\">[24]</a></sup>\n",
      "</td>\n",
      "<td><a href=\"/wiki/Low_Earth_orbit\" title=\"Low Earth orbit\">LEO</a>\n",
      "</td>\n",
      "<td><a href=\"/wiki/Orbcomm\" title=\"Orbcomm\">Orbcomm</a>\n",
      "</td>\n",
      "<td class=\"table-partial\" style=\"background: #FE9; vertical-align: middle; text-align: center;\">Partial failure<sup class=\"reference\" id=\"cite_ref-nyt-20121030_31-0\"><a href=\"#cite_note-nyt-20121030-31\">[25]</a></sup>\n",
      "</td></tr>\n",
      "<tr>\n",
      "<td colspan=\"9\">CRS-1 was successful, but the <a href=\"/wiki/Secondary_payload\" title=\"Secondary payload\">secondary payload</a> was inserted into an abnormally low orbit and subsequently lost. This was due to one of the nine <a href=\"/wiki/SpaceX_Merlin\" title=\"SpaceX Merlin\">Merlin engines</a> shutting down during the launch, and NASA declining a second reignition, as per <a href=\"/wiki/International_Space_Station\" title=\"International Space Station\">ISS</a> visiting vehicle safety rules, the primary payload owner is contractually allowed to decline a second reignition. NASA stated that this was because SpaceX could not guarantee a high enough likelihood of the second stage completing the second burn successfully which was required to avoid any risk of secondary payload's collision with the ISS.<sup class=\"reference\" id=\"cite_ref-OrbcommTotalLoss_32-0\"><a href=\"#cite_note-OrbcommTotalLoss-32\">[26]</a></sup><sup class=\"reference\" id=\"cite_ref-sn20121011_33-0\"><a href=\"#cite_note-sn20121011-33\">[27]</a></sup><sup class=\"reference\" id=\"cite_ref-34\"><a href=\"#cite_note-34\">[28]</a></sup>\n",
      "</td></tr>\n",
      "<tr>\n",
      "<th rowspan=\"2\" scope=\"row\" style=\"text-align:center;\">5\n",
      "</th>\n",
      "<td>1 March 2013,<br/>15:10\n",
      "</td>\n",
      "<td><a href=\"/wiki/Falcon_9_v1.0\" title=\"Falcon 9 v1.0\">F9 v1.0</a><sup class=\"reference\" id=\"cite_ref-MuskMay2012_13-4\"><a href=\"#cite_note-MuskMay2012-13\">[7]</a></sup><br/>B0007.1<sup class=\"reference\" id=\"cite_ref-block_numbers_14-4\"><a href=\"#cite_note-block_numbers-14\">[8]</a></sup>\n",
      "</td>\n",
      "<td><a href=\"/wiki/Cape_Canaveral_Space_Force_Station\" title=\"Cape Canaveral Space Force Station\">CCAFS</a>,<br/><a href=\"/wiki/Cape_Canaveral_Space_Launch_Complex_40\" title=\"Cape Canaveral Space Launch Complex 40\">SLC-40</a>\n",
      "</td>\n",
      "<td><a href=\"/wiki/SpaceX_CRS-2\" title=\"SpaceX CRS-2\">SpaceX CRS-2</a><sup class=\"reference\" id=\"cite_ref-sxManifest20120925_28-1\"><a href=\"#cite_note-sxManifest20120925-28\">[22]</a></sup><br/>(Dragon C104)\n",
      "</td>\n",
      "<td>4,877 kg (10,752 lb)\n",
      "</td>\n",
      "<td><a href=\"/wiki/Low_Earth_orbit\" title=\"Low Earth orbit\">LEO</a> (<a class=\"mw-redirect\" href=\"/wiki/ISS\" title=\"ISS\">ISS</a>)\n",
      "</td>\n",
      "<td><a href=\"/wiki/NASA\" title=\"NASA\">NASA</a> (<a href=\"/wiki/Commercial_Resupply_Services\" title=\"Commercial Resupply Services\">CRS</a>)\n",
      "</td>\n",
      "<td class=\"table-success\" style=\"background: #9EFF9E; vertical-align: middle; text-align: center;\">Success\n",
      "</td>\n",
      "<td class=\"table-noAttempt\" style=\"background: #EEE; vertical-align: middle; white-space: nowrap; text-align: center;\">No attempt\n",
      "</td></tr>\n",
      "<tr>\n",
      "<td colspan=\"9\">Last launch of the original Falcon 9 v1.0 <a href=\"/wiki/Launch_vehicle\" title=\"Launch vehicle\">launch vehicle</a>, first use of the unpressurized trunk section of Dragon.<sup class=\"reference\" id=\"cite_ref-sxf9_20110321_35-0\"><a href=\"#cite_note-sxf9_20110321-35\">[29]</a></sup>\n",
      "</td></tr>\n",
      "<tr>\n",
      "<th rowspan=\"2\" scope=\"row\" style=\"text-align:center;\">6\n",
      "</th>\n",
      "<td>29 September 2013,<br/>16:00<sup class=\"reference\" id=\"cite_ref-pa20130930_36-0\"><a href=\"#cite_note-pa20130930-36\">[30]</a></sup>\n",
      "</td>\n",
      "<td><a href=\"/wiki/Falcon_9_v1.1\" title=\"Falcon 9 v1.1\">F9 v1.1</a><sup class=\"reference\" id=\"cite_ref-MuskMay2012_13-5\"><a href=\"#cite_note-MuskMay2012-13\">[7]</a></sup><br/>B1003<sup class=\"reference\" id=\"cite_ref-block_numbers_14-5\"><a href=\"#cite_note-block_numbers-14\">[8]</a></sup>\n",
      "</td>\n",
      "<td><a class=\"mw-redirect\" href=\"/wiki/Vandenberg_Air_Force_Base\" title=\"Vandenberg Air Force Base\">VAFB</a>,<br/><a href=\"/wiki/Vandenberg_Space_Launch_Complex_4\" title=\"Vandenberg Space Launch Complex 4\">SLC-4E</a>\n",
      "</td>\n",
      "<td><a href=\"/wiki/CASSIOPE\" title=\"CASSIOPE\">CASSIOPE</a><sup class=\"reference\" id=\"cite_ref-sxManifest20120925_28-2\"><a href=\"#cite_note-sxManifest20120925-28\">[22]</a></sup><sup class=\"reference\" id=\"cite_ref-CASSIOPE_MDA_37-0\"><a href=\"#cite_note-CASSIOPE_MDA-37\">[31]</a></sup>\n",
      "</td>\n",
      "<td>500 kg (1,100 lb)\n",
      "</td>\n",
      "<td><a href=\"/wiki/Polar_orbit\" title=\"Polar orbit\">Polar orbit</a> <a href=\"/wiki/Low_Earth_orbit\" title=\"Low Earth orbit\">LEO</a>\n",
      "</td>\n",
      "<td><a href=\"/wiki/Maxar_Technologies\" title=\"Maxar Technologies\">MDA</a>\n",
      "</td>\n",
      "<td class=\"table-success\" style=\"background: #9EFF9E; vertical-align: middle; text-align: center;\">Success<sup class=\"reference\" id=\"cite_ref-pa20130930_36-1\"><a href=\"#cite_note-pa20130930-36\">[30]</a></sup>\n",
      "</td>\n",
      "<td class=\"table-no2\" style=\"background: #FFE3E3; color: black; vertical-align: middle; text-align: center;\">Uncontrolled<br/><small>(ocean)</small><sup class=\"reference\" id=\"cite_ref-ocean_landing_38-0\"><a href=\"#cite_note-ocean_landing-38\">[d]</a></sup>\n",
      "</td></tr>\n",
      "<tr>\n",
      "<td colspan=\"9\">First commercial mission with a private customer, first launch from Vandenberg, and demonstration flight of Falcon 9 v1.1 with an improved 13-tonne to LEO capacity.<sup class=\"reference\" id=\"cite_ref-sxf9_20110321_35-1\"><a href=\"#cite_note-sxf9_20110321-35\">[29]</a></sup> After separation from the second stage carrying Canadian commercial and scientific satellites, the first stage booster performed a controlled reentry,<sup class=\"reference\" id=\"cite_ref-39\"><a href=\"#cite_note-39\">[32]</a></sup> and an <a href=\"/wiki/Falcon_9_first-stage_landing_tests\" title=\"Falcon 9 first-stage landing tests\">ocean touchdown test</a> for the first time. This provided good test data, even though the booster started rolling as it neared the ocean, leading to the shutdown of the central engine as the roll depleted it of fuel, resulting in a hard impact with the ocean.<sup class=\"reference\" id=\"cite_ref-pa20130930_36-2\"><a href=\"#cite_note-pa20130930-36\">[30]</a></sup> This was the first known attempt of a rocket engine being lit to perform a supersonic retro propulsion, and allowed SpaceX to enter a public-private partnership with <a href=\"/wiki/NASA\" title=\"NASA\">NASA</a> and its Mars entry, descent, and landing technologies research projects.<sup class=\"reference\" id=\"cite_ref-40\"><a href=\"#cite_note-40\">[33]</a></sup> <small>(<a href=\"#Maiden_flight_of_v1.1\">more details below</a>)</small>\n",
      "</td></tr>\n",
      "<tr>\n",
      "<th rowspan=\"2\" scope=\"row\" style=\"text-align:center;\">7\n",
      "</th>\n",
      "<td>3 December 2013,<br/>22:41<sup class=\"reference\" id=\"cite_ref-sfn_wwls20130624_41-0\"><a href=\"#cite_note-sfn_wwls20130624-41\">[34]</a></sup>\n",
      "</td>\n",
      "<td><a href=\"/wiki/Falcon_9_v1.1\" title=\"Falcon 9 v1.1\">F9 v1.1</a><br/>B1004\n",
      "</td>\n",
      "<td><a href=\"/wiki/Cape_Canaveral_Space_Force_Station\" title=\"Cape Canaveral Space Force Station\">CCAFS</a>,<br/><a href=\"/wiki/Cape_Canaveral_Space_Launch_Complex_40\" title=\"Cape Canaveral Space Launch Complex 40\">SLC-40</a>\n",
      "</td>\n",
      "<td><a href=\"/wiki/SES-8\" title=\"SES-8\">SES-8</a><sup class=\"reference\" id=\"cite_ref-sxManifest20120925_28-3\"><a href=\"#cite_note-sxManifest20120925-28\">[22]</a></sup><sup class=\"reference\" id=\"cite_ref-spx-pr_42-0\"><a href=\"#cite_note-spx-pr-42\">[35]</a></sup><sup class=\"reference\" id=\"cite_ref-aw20110323_43-0\"><a href=\"#cite_note-aw20110323-43\">[36]</a></sup>\n",
      "</td>\n",
      "<td>3,170 kg (6,990 lb)\n",
      "</td>\n",
      "<td><a href=\"/wiki/Geostationary_transfer_orbit\" title=\"Geostationary transfer orbit\">GTO</a>\n",
      "</td>\n",
      "<td><a href=\"/wiki/SES_S.A.\" title=\"SES S.A.\">SES</a>\n",
      "</td>\n",
      "<td class=\"table-success\" style=\"background: #9EFF9E; vertical-align: middle; text-align: center;\">Success<sup class=\"reference\" id=\"cite_ref-SNMissionStatus7_44-0\"><a href=\"#cite_note-SNMissionStatus7-44\">[37]</a></sup>\n",
      "</td>\n",
      "<td class=\"table-noAttempt\" style=\"background: #EEE; vertical-align: middle; white-space: nowrap; text-align: center;\">No attempt<br/><sup class=\"reference\" id=\"cite_ref-sf10120131203_45-0\"><a href=\"#cite_note-sf10120131203-45\">[38]</a></sup>\n",
      "</td></tr>\n",
      "<tr>\n",
      "<td colspan=\"9\">First <a href=\"/wiki/Geostationary_transfer_orbit\" title=\"Geostationary transfer orbit\">Geostationary transfer orbit</a> (GTO) launch for Falcon 9,<sup class=\"reference\" id=\"cite_ref-spx-pr_42-1\"><a href=\"#cite_note-spx-pr-42\">[35]</a></sup> and first successful reignition of the second stage.<sup class=\"reference\" id=\"cite_ref-46\"><a href=\"#cite_note-46\">[39]</a></sup> SES-8 was inserted into a <a href=\"/wiki/Geostationary_transfer_orbit\" title=\"Geostationary transfer orbit\">Super-Synchronous Transfer Orbit</a> of 79,341 km (49,300 mi) in apogee with an <a href=\"/wiki/Orbital_inclination\" title=\"Orbital inclination\">inclination</a> of 20.55° to the <a href=\"/wiki/Equator\" title=\"Equator\">equator</a>.\n",
      "</td></tr></tbody></table>\n"
     ]
    }
   ],
   "source": [
    "# Let's print the third table and check its content\n",
    "first_launch_table = html_tables[2]\n",
    "print(first_launch_table)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "You should able to see the columns names embedded in the table header elements `<th>` as follows:\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "```\n",
    "<tr>\n",
    "<th scope=\"col\">Flight No.\n",
    "</th>\n",
    "<th scope=\"col\">Date and<br/>time (<a href=\"/wiki/Coordinated_Universal_Time\" title=\"Coordinated Universal Time\">UTC</a>)\n",
    "</th>\n",
    "<th scope=\"col\"><a href=\"/wiki/List_of_Falcon_9_first-stage_boosters\" title=\"List of Falcon 9 first-stage boosters\">Version,<br/>Booster</a> <sup class=\"reference\" id=\"cite_ref-booster_11-0\"><a href=\"#cite_note-booster-11\">[b]</a></sup>\n",
    "</th>\n",
    "<th scope=\"col\">Launch site\n",
    "</th>\n",
    "<th scope=\"col\">Payload<sup class=\"reference\" id=\"cite_ref-Dragon_12-0\"><a href=\"#cite_note-Dragon-12\">[c]</a></sup>\n",
    "</th>\n",
    "<th scope=\"col\">Payload mass\n",
    "</th>\n",
    "<th scope=\"col\">Orbit\n",
    "</th>\n",
    "<th scope=\"col\">Customer\n",
    "</th>\n",
    "<th scope=\"col\">Launch<br/>outcome\n",
    "</th>\n",
    "<th scope=\"col\"><a href=\"/wiki/Falcon_9_first-stage_landing_tests\" title=\"Falcon 9 first-stage landing tests\">Booster<br/>landing</a>\n",
    "</th></tr>\n",
    "```\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Next, we just need to iterate through the `<th>` elements and apply the provided `extract_column_from_header()` to extract column name one by one\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 15,
   "metadata": {
    "tags": []
   },
   "outputs": [],
   "source": [
    "column_names = []\n",
    "\n",
    "# Apply find_all() function with `th` element on first_launch_table\n",
    "# Iterate each th element and apply the provided extract_column_from_header() to get a column name\n",
    "# Append the Non-empty column name (`if name is not None and len(name) > 0`) into a list called column_names\n",
    "for element in first_launch_table.find_all('th'):\n",
    "    name = extract_column_from_header(element)\n",
    "    if name is not None and len(name) > 0:\n",
    "        column_names.append(name)\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Check the extracted column names\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 16,
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "['Flight No.', 'Date and time ( )', 'Launch site', 'Payload', 'Payload mass', 'Orbit', 'Customer', 'Launch outcome']\n"
     ]
    }
   ],
   "source": [
    "print(column_names)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## TASK 3: Create a data frame by parsing the launch HTML tables\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "We will create an empty dictionary with keys from the extracted column names in the previous task. Later, this dictionary will be converted into a Pandas dataframe\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 17,
   "metadata": {
    "tags": []
   },
   "outputs": [],
   "source": [
    "launch_dict= dict.fromkeys(column_names)\n",
    "\n",
    "# Remove an irrelvant column\n",
    "del launch_dict['Date and time ( )']\n",
    "\n",
    "# Let's initial the launch_dict with each value to be an empty list\n",
    "launch_dict['Flight No.'] = []\n",
    "launch_dict['Launch site'] = []\n",
    "launch_dict['Payload'] = []\n",
    "launch_dict['Payload mass'] = []\n",
    "launch_dict['Orbit'] = []\n",
    "launch_dict['Customer'] = []\n",
    "launch_dict['Launch outcome'] = []\n",
    "# Added some new columns\n",
    "launch_dict['Version Booster']=[]\n",
    "launch_dict['Booster landing']=[]\n",
    "launch_dict['Date']=[]\n",
    "launch_dict['Time']=[]"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Next, we just need to fill up the `launch_dict` with launch records extracted from table rows.\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Usually, HTML tables in Wiki pages are likely to contain unexpected annotations and other types of noises, such as reference links `B0004.1[8]`, missing values `N/A [e]`, inconsistent formatting, etc.\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "To simplify the parsing process, we have provided an incomplete code snippet below to help you to fill up the `launch_dict`. Please complete the following code snippet with TODOs or you can choose to write your own logic to parse all launch tables:\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "extracted_row = 0\n",
    "#Extract each table \n",
    "for table_number,table in enumerate(soup.find_all('table',\"wikitable plainrowheaders collapsible\")):\n",
    "   # get table row \n",
    "    for rows in table.find_all(\"tr\"):\n",
    "        #check to see if first table heading is as number corresponding to launch a number \n",
    "        if rows.th:\n",
    "            if rows.th.string:\n",
    "                flight_number=rows.th.string.strip()\n",
    "                flag=flight_number.isdigit()\n",
    "        else:\n",
    "            flag=False\n",
    "        #get table element \n",
    "        row=rows.find_all('td')\n",
    "        #if it is number save cells in a dictonary \n",
    "        if flag:\n",
    "            extracted_row += 1\n",
    "            # Flight Number value\n",
    "            # TODO: Append the flight_number into launch_dict with key `Flight No.`\n",
    "            #print(flight_number)\n",
    "            datatimelist=date_time(row[0])\n",
    "            \n",
    "            # Date value\n",
    "            # TODO: Append the date into launch_dict with key `Date`\n",
    "            date = datatimelist[0].strip(',')\n",
    "            #print(date)\n",
    "            \n",
    "            # Time value\n",
    "            # TODO: Append the time into launch_dict with key `Time`\n",
    "            time = datatimelist[1]\n",
    "            #print(time)\n",
    "              \n",
    "            # Booster version\n",
    "            # TODO: Append the bv into launch_dict with key `Version Booster`\n",
    "            bv=booster_version(row[1])\n",
    "            if not(bv):\n",
    "                bv=row[1].a.string\n",
    "            print(bv)\n",
    "            \n",
    "            # Launch Site\n",
    "            # TODO: Append the bv into launch_dict with key `Launch Site`\n",
    "            launch_site = row[2].a.string\n",
    "            #print(launch_site)\n",
    "            \n",
    "            # Payload\n",
    "            # TODO: Append the payload into launch_dict with key `Payload`\n",
    "            payload = row[3].a.string\n",
    "            #print(payload)\n",
    "            \n",
    "            # Payload Mass\n",
    "            # TODO: Append the payload_mass into launch_dict with key `Payload mass`\n",
    "            payload_mass = get_mass(row[4])\n",
    "            #print(payload)\n",
    "            \n",
    "            # Orbit\n",
    "            # TODO: Append the orbit into launch_dict with key `Orbit`\n",
    "            orbit = row[5].a.string\n",
    "            #print(orbit)\n",
    "            \n",
    "            # Customer\n",
    "            # TODO: Append the customer into launch_dict with key `Customer`\n",
    "            customer = row[6].a.string\n",
    "            #print(customer)\n",
    "            \n",
    "            # Launch outcome\n",
    "            # TODO: Append the launch_outcome into launch_dict with key `Launch outcome`\n",
    "            launch_outcome = list(row[7].strings)[0]\n",
    "            #print(launch_outcome)\n",
    "            \n",
    "            # Booster landing\n",
    "            # TODO: Append the launch_outcome into launch_dict with key `Booster landing`\n",
    "            booster_landing = landing_status(row[8])\n",
    "            #print(booster_landing)\n",
    "            "
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "After you have fill in the parsed launch record values into `launch_dict`, you can create a dataframe from it.\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "df=pd.DataFrame(launch_dict)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "We can now export it to a <b>CSV</b> for the next section, but to make the answers consistent and in case you have difficulties finishing this lab. \n",
    "\n",
    "Following labs will be using a provided dataset to make each lab independent. \n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "<code>df.to_csv('spacex_web_scraped.csv', index=False)</code>\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Authors\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "<a href=\"https://www.linkedin.com/in/yan-luo-96288783/?utm_medium=Exinfluencer&utm_source=Exinfluencer&utm_content=000026UJ&utm_term=10006555&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMDS0321ENSkillsNetwork865-2023-01-01\">Yan Luo</a>\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "<a href=\"https://www.linkedin.com/in/nayefaboutayoun/?utm_medium=Exinfluencer&utm_source=Exinfluencer&utm_content=000026UJ&utm_term=10006555&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMDS0321ENSkillsNetwork865-2023-01-01\">Nayef Abou Tayoun</a>\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Change Log\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "| Date (YYYY-MM-DD) | Version | Changed By | Change Description      |\n",
    "| ----------------- | ------- | ---------- | ----------------------- |\n",
    "| 2021-06-09        | 1.0     | Yan Luo    | Tasks updates           |\n",
    "| 2020-11-10        | 1.0     | Nayef      | Created the initial version |\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Copyright © 2021 IBM Corporation. All rights reserved.\n"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python",
   "language": "python",
   "name": "conda-env-python-py"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.12"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
