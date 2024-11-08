FROM tomcat:9.0-jdk8

# 기본 Tomcat 웹 애플리케이션 제거
RUN rm -rf /usr/local/tomcat/webapps/*

# WAR 파일을 Tomcat의 webapps 디렉토리에 ROOT.war로 추가
ADD target/log4shell-1.0-SNAPSHOT.war /usr/local/tomcat/webapps/ROOT.war

# Tomcat이 사용하는 8080 포트를 열어줍니다
EXPOSE 8080

# Tomcat을 포그라운드에서 실행
CMD ["catalina.sh", "run"]
