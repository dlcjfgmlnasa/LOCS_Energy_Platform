import dotenv from "dotenv";
dotenv.config();
import { ConnectionOptions } from "typeorm";

const ConnectionOptions: ConnectionOptions = {
  type: "mysql",
  database: process.env.DB_NAME || "",
  username: process.env.DB_USERNAME || "",
  password: process.env.DB_PASSWORD || "",
  host: process.env.DB_HOST || "localhost",
  port: Number(process.env.DB_PORT),
  synchronize: true
//   entities: ["entities/**/*.*"]
}

export default ConnectionOptions;