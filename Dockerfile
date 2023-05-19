# build

# We used a multi-stage build to reduce the final image size. 
# Essentially, build-vue is a temporary image that's used to generate a production build of the Vue app. 
# The production static files are then copied over to the production image and the build-vue image is discarded.
FROM node:20 as build-vue
WORKDIR /app
ENV PATH /app/node_modules/.bin:$PATH
COPY ./client/package*.json ./
RUN npm install
COPY ./client .
RUN npm run build

# production

# The production image extends the nginx:stable-alpine image by installing Python, copying over the static files from the build-vue image, 
# copying over our Nginx config, installing the requirements, and running Gunicorn along with Nginx.
FROM nginx:stable-alpine as production
WORKDIR /app
RUN apk update && apk add --no-cache python3 && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
    rm -r /root/.cache
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
COPY --from=build-vue /app/dist /usr/share/nginx/html
COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf
COPY ./server/requirements.txt .
RUN pip install -r requirements.txt
RUN pip install gunicorn
COPY ./server .
# Take note of the sed -i -e 's/$PORT/'"$PORT"'/g' /etc/nginx/conf.d/default.conf command. 
# Here, we're using sed to replace $PORT in the default.conf file with the environment variable PORT supplied by Heroku.
CMD gunicorn -b 0.0.0.0:5000 app:app --daemon && \
      sed -i -e 's/$PORT/'"$PORT"'/g' /etc/nginx/conf.d/default.conf && \
      nginx -g 'daemon off;'