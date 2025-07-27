REPORT_MODEL = 'gpt-4'
LLM_MODEL = 'gpt-4o-mini'
TEMPERATURE = 0
MAX_TOKENS_600 = 600
MAX_TOKENS_800 = 800


PROMPT = '''You are an AI safety inspector. You are shown a construction site image.

            Your only task is to check if the person in the image is wearing any of the following PPE (personal protective equipment):

            - A hard hat
            - A high-visibility vest
            - High-visibility pants
            - No PPE at all

            Only include items in the output if the model's confidence is greater than 0.5.  
            If confidence is ≤ 0.5, set `<prediction>' to 0 and still include the actual confidence value.
            Predictions must be based only on visual evidence in the image. 
            Do not assume PPE is present unless it is clearly visible with confidence > 0.5.
            Please respond using **only** the following XML structure. Do not include any extra text, explanation, or summaries. 
            Return only the content starting with <output> and ending with </output>.

            <output>
                <has-hard-hat>
                    <prediction>{1 or 0}</prediction>
                    <confidence>{0.0 - 1.0}</confidence>
                </has-hard-hat>
                <has-high-vis-pants>
                    <prediction>{1 or 0}</prediction>
                    <confidence>{0.0 - 1.0}</confidence>
                </has-high-vis-pants>
                <has-high-vis-vest>
                    <prediction>{1 or 0}</prediction>
                    <confidence>{0.0 - 1.0}</confidence>
                </has-high-vis-vest>
                <no-ppe>
                    <prediction>{1 or 0}</prediction>
                    <confidence>{0.0 - 1.0}</confidence>
                </no-ppe>
            </output>'''


def get_test_prompt(vision_data, weather_data):

    return f'''
        You are a safety analyst AI. You are given two JSON objects:

        1. One contains detections of PPE violations, keyed by timestamp (format: "YYYY:MM:DD HH:MM:SS"), with each entry containing an image path and a list of detected safety risks like "No PP Equipment", "No Hard Hat", "No High Vis Pants", etc.

        2. The other contains weather risk events, keyed by timestamp (format: "YYYY-MM-DDTHH:00"), with weather indicators like "shortwave_radiation" or "relativehumidity_2m".

        Your task is to:
        - Match entries from both datasets that occur in the same **hour** (you can ignore minutes and seconds).
        - Report when both a **PPE risk** **OR** a **weather risk** occur.
        - For each match, include:
        - the timestamp
        - image_path
        - the specific PPE risks **OR**
        - the specific weather risks
        - recommendations for safety measures.

        Please respond using **only** the following XML structure. Do not include any extra text, explanation, or summaries
        except for **safety recommendation**. 
        Return only the content starting with <incident> and ending with </incident>.

        <incidents>
            <incident>
                <timestamp>2025-07-15T08:00</timestamp>
                <image_path>example.jpg</image_path>
                <ppe_risks>
                    <risk>No PP Equipment</risk>
                    <risk>No High Vis Vest</risk>
                </ppe_risks>
                <weather_risks>
                    <risk>shortwave_radiation</risk>
                </weather_risks>
                <recommendation>Safety recommendation</recommendation>
            </incident>
        </incidents>

        Now, analyze the two datasets below and list any hours where risks happened at the same time.

        PPE Risk Summary:
        {vision_data}

        Weather Risk Summary:
        {weather_data}
        '''


RESOLUTION = 'high'