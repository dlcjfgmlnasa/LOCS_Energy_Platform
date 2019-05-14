import "reflect-metadata";
import express from "express";
import dotenv from "dotenv";
import { createConnection, ConnectionOptions } from "typeorm";
import helmet from "helmet";
import cors from "cors";
import bodyParser from "body-parser";
import logger from "morgan";
import routes from "./routes";

dotenv.config();

// DataBase Settings
const ConnectionOptions: ConnectionOptions = {
  type: "mysql",
  database: process.env.DB_NAME || "",
  username: process.env.DB_USERNAME || "",
  password: process.env.DB_PASSWORD || "",
  host: process.env.DB_HOST || "localhost",
  port: Number(process.env.DB_PORT),
  synchronize: true,
  logging: false,
  entities: [`${__dirname}/entities/*.*`]
}

const app = express();

// Call Middleware
app.use(cors());                    /* cors - Enable cross-origin Requests */
app.use(helmet());                  /* helmet - Help us to secure our application by setting various HTTP headers */
app.use(bodyParser.json());         /* body-parser - Parses the client’s request from json into javascript objects */
app.use(logger('dev'))

// Set all routes from routes folder
app.use('/', routes);

createConnection(ConnectionOptions)
  .then(connection => {
    // Create a new express application instance
    app.listen(Number(process.env.HOST_PORT), String(process.env.HOST_DOMAIN), () => {
      console.log(`app listening on http://${process.env.HOST_DOMAIN}:${process.env.HOST_PORT}`);
    });
  })
  .catch(error => console.log(error));