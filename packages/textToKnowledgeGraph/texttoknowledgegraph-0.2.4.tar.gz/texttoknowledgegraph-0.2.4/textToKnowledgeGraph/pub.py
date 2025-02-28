import os
import requests
import logging
from lxml import etree


def download_pubtator_xml(pmc_id, output_dir):
    """
    Downloads the XML file from PubTator API using PMCID and saves it in the specified output directory.
    """
    # Construct the PubTator API URL
    url = f"https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/pmc_export/biocxml?pmcids={pmc_id}"

    # Make the request
    response = requests.get(url)
    if response.status_code == 200:
        logging.info(f"Successfully downloaded XML for PMCID {pmc_id}.")
        file_path = os.path.join(output_dir, f"pmc{pmc_id}.xml")

        # Save the file in the existing output directory
        with open(file_path, "wb") as f:
            f.write(response.content)
        return file_path
    else:
        logging.error(f"Failed to download XML for PMCID {pmc_id}. Status code: {response.status_code}")
        return None


def get_pubtator_paragraphs(file_path):
    """
    Extracts paragraphs from a PubTator XML file,
    ensuring text represents full paragraphs or abstract-like content.

    Only includes passages that are of sufficient length.

    :param file_path: Path to the PubTator XML file.
    :return: A dictionary with numbered paragraphs as keys and values containing text.
    """
    tree = etree.parse(file_path)
    root = tree.getroot()

    paragraphs_dict = {}
    passage_elements = root.findall('.//passage')
    paragraph_number = 0

    for passage in passage_elements:
        # Check section type
        section_type = passage.findtext('infon[@key="section_type"]', "").lower()

        # Include sections that are meaningful (abstracts, paragraphs, introduction, etc.)
        if section_type in ['ref', 'title']:
            continue  # Skip non-content sections

        # Extract the passage text
        text_elem = passage.find('text')
        passage_text = text_elem.text.strip() if text_elem is not None else ""
        if len(passage_text) < 20:  # Skip overly short texts
            continue

        # add the paragraph to the dictionary
        paragraphs_dict[str(paragraph_number)] = {
            'text': passage_text
        }
        paragraph_number += 1

    return paragraphs_dict
