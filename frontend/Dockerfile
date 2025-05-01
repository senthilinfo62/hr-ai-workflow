FROM node:18-alpine

WORKDIR /app

# Install dependencies
COPY package.json .
RUN npm install

# Copy application code
COPY . .

# Run linting during build (commented out for now)
# RUN npm run lint

# Start the application
CMD ["npm", "run", "dev"]
