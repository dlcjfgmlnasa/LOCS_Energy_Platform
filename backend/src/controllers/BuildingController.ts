import { Request, Response } from "express";
import { getRepository } from "typeorm";
import { Building } from "../entities/Building";


/* Building Model (Build.ts) Controller */
class BuildingController {
  public getBldList = async (req: Request, res: Response) => {
    try{
      const list = await getRepository(Building)
      .createQueryBuilder("building")
      .select("building.name")
      .addSelect("building.id")
      .getMany();

      res.json(list);
    }
    catch(e){
      res.status(404).json({ message: e.message });
      throw new Error(e);
    }
  }

  public getBldBrokenList = async (req: Request, res: Response) => {
    try{
      const list = await getRepository(Building)
      .createQueryBuilder("building")
      .select("building.name")
      .addSelect("building.id")
      .where("building.id IN (:authors)", { authors: [1]})
      .getMany();

      res.json(list);
    }
    catch(e){
      res.status(404).json({ message: e.message });
      throw new Error(e);
    }
  }
}

export default BuildingController;