# Immagine Node
FROM node:20-alpine

# Directory di lavoro
WORKDIR /app

# Copia file
COPY package.json .
COPY package-lock.json* ./

# Installa dipendenze
RUN npm install

# Copia sorgenti
COPY . .

# Espone porta
EXPOSE 3000

# Avvia Vite
CMD ["npm", "run", "dev"]
