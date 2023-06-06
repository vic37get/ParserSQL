import re 

texto = 'CREATE TABLE <id> (<id> <tipo> [, <id> <tipo>]*);'
texto = re.sub('\(',' ( ', texto)
texto = re.sub('\)', ' ) ', texto)

texto = re.sub('\[',' [ ', texto)
texto = re.sub('\]', ' ] ', texto)

texto = re.sub(';', ' ; ', texto)

texto = re.sub('(\s)', '\s', texto)


print(texto)

