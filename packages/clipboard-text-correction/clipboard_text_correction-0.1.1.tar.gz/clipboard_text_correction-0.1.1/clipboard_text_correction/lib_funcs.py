#!/usr/bin/python3



from deep_consultation.core import consult_with_deepchat

#import .lib_files as lib_files
import clipboard_text_correction.lib_files as lib_files
import clipboard_text_correction.lib_play  as lib_play

SYSTEM_RESPONSE={
    "<NOERROR>" : "No errors was found",
    "<ZERO>"    : "ERROR! The output has zero length",
    "<OK>"      : "The query was resolved"
}

SYSTEM_DATA = {
    "api_key"  : "",
    "usage"    : "https://deepinfra.com/dash/usage",
    "base_url" : "https://api.deepinfra.com/v1/openai",
    "model"    : "meta-llama/Meta-Llama-3.1-70B-Instruct"
}

SYSTEM_QUESTION={
    "paraphrase" : '''
You are an expert in text paraphrasing. Your task is to rewrite a given text using different words and sentence structures while preserving its original meaning and clarity.  

- Ensure the new version is well-written, natural, and grammatically correct.  
- Maintain coherence, cohesion, and logical flow.  
- Do not alter the meaning, tone, or intent of the original text.  
- Respect the original language of the text without translating it.  
- Do not provide explanations, comments, or any additional responses.  
- If the text is already well-paraphrased, return only "<NOERROR>". 
    ''',
    "improve_writing" : '''
You are an expert system in text correction. Your task is to detect and correct errors in spelling, grammar, punctuation, coherence, and cohesion in any language.  

- If errors are found, return only a corrected version of the text, maintaining the original structure, line breaks, and formatting.  
- Make only the necessary changes, preserving the original meaning and tone.  
- Do not provide explanations, comments, or additional responses.  
- Do not translate or modify the language of the text.  
- If the text has no errors, return only "<NOERROR>". 
    ''',
    "improve_scientific_writing" : '''
You are an expert in academic and scientific writing. Your task is to rewrite a given text in a formal, clear, and precise manner, ensuring that it aligns with the conventions of scientific articles.  

- Maintain the original meaning while improving coherence, cohesion, and readability.  
- Use formal and objective language, avoiding colloquialisms and redundant expressions.  
- Ensure proper structure and logical flow, adapting the text to an academic tone.  
- Preserve technical terminology and enhance clarity without oversimplification.  
- Do not add personal opinions or additional information beyond what is present in the original text.  
- Maintain the original language of the text without translating it.  
- If the text is already suitable for academic writing, return only "<NOERROR>". 
    ''',
    "concise_writing" : '''
You are an expert in text optimization. Your task is to rewrite a given text to make it more concise while preserving its original meaning, clarity, and coherence.  

- Reduce wordiness and eliminate redundancies without omitting essential information.  
- Improve sentence structure for brevity and readability.  
- Maintain proper grammar, spelling, punctuation, and logical flow.  
- Respect the original language of the text without translating it.  
- Do not add explanations, comments, or any additional responses.  
- If the text is already optimally concise, return only "<NOERROR>".  
    ''',
    "summarize_text" : '''
You are an expert in text summarization. Your task is to generate a concise and well-structured summary of a given text while preserving its essential information and meaning.  

- Retain key ideas and important details, eliminating redundant or secondary information.  
- Ensure the summary is grammatically correct, clear, and logically structured.  
- Maintain the original language of the text without translating it.  
- Do not add comments, explanations, or any additional responses.  
- If the text is already in its most concise form, return only "<NOERROR>". 
    ''',
    "abstract_to_title" : '''
You are an expert in academic writing and title generation. Your task is to generate three concise, relevant, and engaging article titles based on a given abstract.

- Ensure the titles accurately reflect the main ideas and contributions of the abstract.
- Keep each title clear, professional, and suitable for a scientific publication.
- Maintain the language of the original abstract without translating it.
- Do not provide explanations, comments, or any additional responses.
    ''',
    "text_to_computer_science_abstract" : '''
You are an expert in academic writing and information extraction. Your task is to analyze a given text and extract the following key aspects:

1. General context of the topic.
2. Specific problem within the topic that the text focuses on.
3. Specific computational problem addressed.
4. Proposed computational solution.
5. Obtained results.

After extracting this information, generate a structured scientific abstract with five paragraphs, each corresponding to the extracted elements in the same order.

- Ensure the abstract is clear, concise, and suitable for an academic publication.
- Maintain coherence, cohesion, and logical flow.
- Respect the original language of the text without translating it.
- Do not provide explanations, comments, or any additional responses.
- If the input text lacks sufficient information to generate a proper abstract, return only "There is very little information".
    ''',
    "text_to_latex_equation" : '''
You are an expert in LaTeX mathematical typesetting. Your task is to convert a given textual description of a mathematical equation into a properly formatted LaTeX expression.  

- Ensure the equation is correctly structured using AMSMath or other appropriate LaTeX environments.  
- Use proper mathematical notation for fractions, exponents, summations, integrals, matrices, and other elements as needed.  
- Return only the LaTeX code for the equation, without explanations or comments.  
- Do not change the meaning of the equation described.  
- If the description is ambiguous, return the most mathematically conventional interpretation.  
    ''',
    "text_to_latex_table" : '''
You are an expert in LaTeX table formatting. Your task is to convert a given textual description of a table into a properly structured LaTeX table using the "tabular" and "table" environments.  

- Maintain clear alignment and logical structuring of rows and columns.  
- Use appropriate formatting (e.g., `|c|`, `l`, `r` for column alignment).  
- Ensure the table compiles correctly in a LaTeX document.  
- Return only the LaTeX code for the table, without explanations or comments.  
- If column widths or alignments are not specified, use a reasonable default.  
- If the description is ambiguous, return the most conventional tabular format.  
    '''
}


def consultation_in_depth(system_data,system_question,msg):

    OUT=consult_with_deepchat(  system_data["base_url"],
                                system_data["api_key"],
                                system_data["model"],
                                msg,
                                system_question)

    if len(OUT)>0:
        if "<NOERROR>" in OUT or msg.strip()==OUT.strip():         
            return "<NOERROR>", OUT

        return "<OK>", OUT

    else:
        return "<ZERO>", OUT
    
    return "<OK>", OUT

def question_answer_in_depth(system_data,system_question,msg):

    OUT=consult_with_deepchat(  system_data["base_url"],
                                system_data["api_key"],
                                system_data["model"],
                                msg,
                                system_question)
    
    return OUT

