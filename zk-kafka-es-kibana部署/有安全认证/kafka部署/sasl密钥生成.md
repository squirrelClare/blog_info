keytool -genkey -keystore kafka.server.keystore.jks -validity 365 -storepass "12hdsQW842QDqw" -keypass "12hdsQW842QDqw" -dname "CN=localhost" -storetype pkcs12
keytool -keystore kafka.server.keystore.jks -certreq -file cert-file -storepass "12hdsQW842QDqw" -keypass "12hdsQW842QDqw"
scp cert-file sshuser@HeadNode0_Name:~/ssl/wnX-cert-sign-request`