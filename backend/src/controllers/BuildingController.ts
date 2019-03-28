import { Request, Response } from "express";


/* Building Model (Build.ts) Controller */
class BuildingController {
  static getOneById = (req: Request, res: Response) => {
    res.send('BuildingController');
    res.status(200);
  }
}

export default BuildingController;