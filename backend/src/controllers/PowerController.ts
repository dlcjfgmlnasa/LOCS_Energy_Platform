import { Request, Response } from "express";
import { getRepository } from "typeorm";
import { Power } from "../entities/Power";

/* Power Model (Power.ts) Controller */
class PowerController {
  public getEngMinute = async (req: Request, res: Response) => {
    try{      
      const list = await getRepository(Power)
      .createQueryBuilder("power")
      .where("power.buildingId = :id ", { id: req.param("id") })
      .andWhere("power.year = 2018")    //추후에 현재 날짜로 변경 되야함
      .andWhere("power.month = 6")
      .andWhere("power.day = 1")
      .getMany();

      res.json(list);
    }
    catch(e){
      res.status(404).json({ message: e.message });
      throw new Error(e);
    }
  }

  public getEngHour = async (req: Request, res: Response) => {
    try{
      const list = await getRepository(Power)
      .createQueryBuilder("power")
      .select("power.hour")
      .addSelect("SUM(power.value)", "value")
      .where("power.buildingId = :id ", { id: req.param("id") })
      .andWhere("power.year = 2018")    //추후에 현재 날짜로 변경 되야함
      .andWhere("power.month = 6")
      .andWhere("power.day = 1")
      .groupBy("power.hour")
      .getRawMany();

      res.json(list);
    }
    catch(e){
      res.status(404).json({ message: e.message });
      throw new Error(e);
    }
  }

  public getEngDay = async (req: Request, res: Response) => {
    try{
      const list = await getRepository(Power)
      .createQueryBuilder("power")
      .select("power.day")
      .addSelect("SUM(power.value)", "value")
      .where("power.buildingId = :id ", { id: req.param("id") })
      .andWhere("power.year = 2018")    //추후에 현재 날짜로 변경 되야함
      .andWhere("power.month = 6")
      .groupBy("power.day")
      .getRawMany();

      res.json(list);
    }
    catch(e){
      res.status(404).json({ message: e.message });
      throw new Error(e);
    }
  }

  public getEngMonth = async (req: Request, res: Response) => {
    try{
      const list = await getRepository(Power)
      .createQueryBuilder("power")
      .select("power.month")
      .addSelect("SUM(power.value)", "value")
      .where("power.buildingId = :id ", { id: req.param("id") })
      .andWhere("power.year = 2018")    //추후에 현재 날짜로 변경 되야함
      .groupBy("power.month")
      .getRawMany();

      res.json(list);
    }
    catch(e){
      res.status(404).json({ message: e.message });
      throw new Error(e);
    }
  }
}

export default PowerController;