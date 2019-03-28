import { Request, Response } from "express";


/* Power Model (Power.ts) Controller */
class PowerController {
  static getOneById = (req: Request, res: Response) => {
    res.send('PowerController');
    res.status(200);
  }
}

export default PowerController;