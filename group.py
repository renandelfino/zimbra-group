#!/usr/bin/python

#coding = UTF-8

#The script will compare the user list from an AD group with the members from a distribution list
#If the user is on AD and not on the list, it will add it to the list
#If the user is on the list but not on AD, it will remove it from the list
#Tested on Zimbra FOSS 8.0 .4

#list dict

#'distribution list name': 'group name on AD'
lists = {
'distribution list name of zimbra': 'CN of group name on AD'
}

scope = 'OU=example,DC=domain,DC=local'
domain = "ad server name"
port = "389"
emaildomain = "example.com.br"
ldapbind = "CN of user in AD"
ldappassword = "passwd of user"

pathtozmprov = "/opt/zimbra/bin/zmprov"

import ldap, string, os, sys
for list, departament in lists.iteritems():
	f = os.popen(pathtozmprov + ' gdlm ' + list + '@' + emaildomain + ' | egrep -v "^$" | grep -v members | grep -v "#"')
	f = f.read().strip('\n')
	#print f
	print ('Verificando lista ' + list +'@'+ emaildomain)

	member_list = []
	member_list = f
	res2 = []

	#print member_list

	l = ldap.initialize("ldap://" + domain + ":" + port)
	l.bind_s(ldapbind,ldappassword)

	res = l.search_s(scope, ldap.SCOPE_SUBTREE, "(&(objectClass=user)(memberOf="+ departament +"))", ['sAMAccountName'])
	#print res

	for (dn, vals) in res:
		accountname = vals['sAMAccountName'][0].lower()
		accountname = accountname + "@" + emaildomain
		print ('Verificando se ' + accountname + ' esta na lista ' + list + '@' + emaildomain)
		if accountname not in member_list:
			print ('Adicionando ' + accountname + ' a lista ' + list + '@' + emaildomain)

		os.system(pathtozmprov + ' adlm %s@%s %s' % (list, emaildomain, accountname))
		res2.append(accountname)


	for value in member_list.splitlines():
		accountname = value.rstrip('')
		if accountname not in res2:
			print ('Removendo '+ accountname + ' da lista ' + list + '@' + emaildomain)
			os.system(pathtozmprov +' rdlm %s@%s %s' % (list,emaildomain,accountname)) 

	#except (ldap.LDAPError) as error_message:
		#print error_message

l.unbind_s()
print "Fim"
exit()
