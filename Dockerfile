FROM node:16 as front
COPY ui /build/
WORKDIR /build
RUN mv .env.template .env
RUN npm install && npm run build

FROM maven:3-jdk-11 as mvn
COPY server /build/
WORKDIR /build
COPY --from=front /build/ui/build/* /build/src/main/resources/public/
RUN mvn package -DskipTests

FROM adoptopenjdk/openjdk11:alpine
ARG VER=0.0.1-SNAPSHOT
ARG USER=validation
ARG USER_ID=810
ARG USER_GROUP=validation
ARG USER_GROUP_ID=810
ARG USER_HOME=/home/${USER}
ENV FOLDER=/tmp/target
ENV APP=validation-storage-${VER}.jar
# create a user group and a user
RUN  addgroup -g ${USER_GROUP_ID} ${USER_GROUP}; \
     adduser -u ${USER_ID} -D -g '' -h ${USER_HOME} -G ${USER_GROUP} ${USER} ;

WORKDIR ${USER_HOME}
COPY --chown=validation:validation --from=mvn /build/target/${APP} ${USER_HOME}
USER validation
ENTRYPOINT ["sh", "-c", "java ${JAVA_OPTS} -jar ${APP}"]