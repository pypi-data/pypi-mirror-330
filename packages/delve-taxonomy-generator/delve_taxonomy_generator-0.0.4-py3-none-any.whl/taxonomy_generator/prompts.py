"""Default prompts used by the agent."""

from langchain_core.prompts import ChatPromptTemplate

LABELER_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """Your task is to use the provided taxonomy to categorize the overall topic or intent of a conversation between a human and an AI assistant.  

First, here is the taxonomy to use:

<taxonomy>
{taxonomy}
</taxonomy>

To complete the task:

1. Carefully read through the entire conversation, paying attention to the key topics discussed and the apparent intents behind the human's messages.

2. Consult the taxonomy and identify the single most relevant category that best captures the overall topic or intent of the conversation. 

3. Write out a chain of reasoning for why you selected that category. Explain how the category fits the content of the conversation, referencing specific statements or passages as evidence. Output this reasoning inside <reasoning></reasoning> tags.

4. If by any chance, no category fits the content nicely, use the category 'Other'.

5. Output the name of the category you chose inside <category></category> tags.

That's it! Remember, choose the single most relevant category. Don't choose multiple categories. Think it through carefully and explain your reasoning before giving your final category choice.
"""),
    
    ("human", """Assign a single category to the following content:

<content>
{content} 
</content>

Respond with your reasoning and category within XML tags. Do not include the number, just the category text.""")
])

TAXONOMY_GENERATION_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """# Instruction

## Context

- **Goal**: Your goal is to cluster the input data into meaningful categories for the given use case.

- **Data**: The input data will be a list of human-AI conversation summaries in XML format, including the following elements:

  - **id**: conversation index.

  - **text**: conversation summary.

- **Use case**: {use_case}

- **Previous feedback**: {feedback}

## Requirements

### User Feedback Integration (CRITICAL)

- You MUST incorporate any previous user feedback into your clustering decisions
- If specific changes were requested, implement them exactly as specified
- If general feedback was given, ensure your clustering reflects those preferences
- If no feedback exists, proceed with standard clustering

### Format

- Output clusters in **XML format** with each cluster as a `<cluster>` element, containing the following sub-elements:

  - **id**: category number starting from 1 in an incremental manner.

  - **name**: category name should be **within {cluster_name_length} words**. It can be either verb phrase or noun phrase, whichever is more appropriate.

  - **description**: category description should be **within {cluster_description_length} words**.

Here is an example of your output:

```xml

<clusters>

  <cluster>

    <id>category id</id>

    <name>category name</name>

    <description>category description</description>

  </cluster>

</clusters>

```

- Total number of categories should be **no more than {max_num_clusters}**.

- Output should be in **English** only.

### Quality

- **User Feedback Alignment**: Clusters MUST align with any provided user feedback and preferences
- **No overlap or contradiction** among the categories.
- **Name** is a concise and clear label for the category. Use only phrases that are specific to each category and avoid those that are common to all categories.
- **Description** differentiates one category from another.
- **Name** and **description** can **accurately** and **consistently** classify new data points **without ambiguity**.
- **Name** and **description** are *consistent with each other*.
- Output clusters match the data as closely as possible, without missing important categories or adding unnecessary ones.
- Output clusters should strive to be orthogonal, providing solid coverage of the target domain.
- Output clusters serve the given use case well.
- Output clusters should be specific and meaningful. Do not invent categories that are not in the data.

# Data

<conversations>

{data_xml}

</conversations>"""),
    ("human", """# Questions

## Q1. Please generate a cluster table from the input data that meets the requirements.

Tips

- **User Feedback is MANDATORY**: You MUST address any previous user feedback in your clustering
- If user feedback was provided, explicitly explain how you've incorporated their specific concerns and suggestions
     
- The cluster table should be a **flat list** of **mutually exclusive** categories. Sort them based on their semantic relatedness.

- Though you should aim for {max_num_clusters} categories, you can have *fewer than {max_num_clusters} categories* in the cluster table;  but **do not exceed the limit.** 

- Be **specific** about each category. **Do not include vague categories** such as "Other", "General", "Unclear", "Miscellaneous" or "Undefined" in the cluster table.

- You can ignore low quality or ambiguous data points.

## Q2. Why did you cluster the data the way you did? Explain your reasoning **within {explanation_length} words**. Include how you addressed any user feedback.

## Provide your answers between the tags: <cluster_table>your generated cluster table with no more than {max_num_clusters} categories</cluster_table>, <explanation>explanation of your reasoning process within {explanation_length} words</explanation>.

# Output""")
])