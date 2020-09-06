FROM node:alpine
WORKDIR /frontend
COPY . /frontend
#ARG API_URL
#ENV REACT_APP_HOST_IP_ADDRESS $API_URL
RUN yarn
CMD ["yarn","start"]