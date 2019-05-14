import { Request, Response } from "express";
// import { getRepository } from "typeorm";
// import { Power } from "../entities/Power";

/* Power Model (Power.ts) Controller */
class PowerController {
  static getOneById = (req: Request, res: Response) => {
    res.send('PowerController');
    res.status(200);
  }
}

export default PowerController;