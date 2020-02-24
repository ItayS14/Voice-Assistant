import spacy

class NotSupportedCommand(Exception):
    pass

nlp = spacy.load('en_core_web_sm')

def parse(text):
    """
    The function is the main nlp parsing, it will return the proper nlp function for that text and nlp doc
    :param text: the text to parse (str)
    :return: tupple - (doc, function)
    """
    command_dict = {
    'exchange': nlp_coin_exchange,
    'translate': None, # Change to translate nlp later
    'say': None, # Also translate nlp
    'tell': nlp_wiki    
    }
    wh_dict = {
        'what': nlp_wiki,
        'who': nlp_wiki,
        'where': nlp_wiki,
        'which': nlp_wiki,
    }
    how_dict = {
        'much': nlp_coin_exchange,
        'many': nlp_coin_exchange, # might change
        'does': nlp_wiki,
        'do': None # Translate
    }

    doc = nlp(text) # Maybe disable some pipes later
    first_token = doc[0].lower_
    if doc[-1].text == '?' or first_token in wh_dict.keys():
        return (wh_dict[first_token], doc)
    if first_token == 'how':
        return (how_dict[doc[1].text], doc)
    # Checking if the first word is a VERB might not work
    if first_token not in command_dict.keys():
        raise NotSupportedCommand
    return (command_dict[first_token], doc)


def nlp_wiki(text):
    """
    The function will parse wiki question and return the parameter from the text query
    :param text: the query to parse (str - for now)
    :return: the parameter (str)
    """
    doc = nlp(text)
    for word in doc:
        if word.pos_ == 'AUX':
            return doc[word.i + 1:].text.replace('?', '')
    r = [span.text for span in doc.noun_chunks] # In case that the sentence had no auxilary verbs grouping all noun chunks except the first one
    return ' '.join(r[1:])    


def nlp_coin_exchange(text): #TODO: return currency code
    """
    The function will parse exchange query and return the parameters found
    :param text: the query to parse (str - for now)
    :return: dictionary dictionary that contains the parameters (from_coin, to_coin, _amoun) 
    """
    doc = nlp(text)
    from_c = amount = to_c = None
    for noun in doc.noun_chunks: #root of the noun chunks will be always the currency
        if noun.root.i > 0 and doc[noun.root.i - 1].pos_ == 'NUM': # if there was a number before the currency it indicates that that's the part to exchange
            from_c = noun.root
            amount = doc[noun.root.i - 1]
        else:
            to_c = noun.root
    
    if not (from_c and amount and to_c):
        return ProtocolErrors.INVALID_PARAMETERS_ERROR
    return dict(from_coin=from_c, to_coin=to_c, amount=amount)

def main():
    #print(parse('Translate hello to hebrew'))
    print(parse('Exchange 4 shekels to euro'))
    print(parse('Tell me about world war 1'))
    print(parse('Who was U.s first president'))
    print(parse('How much dollars is 4 shekels'))
    print(parse('How does a car work'))


if __name__ == "__main__":
    main()
