import {
  BaseEntity,
  Entity,
  Column,
  CreateDateColumn,
  ManyToOne,
  PrimaryGeneratedColumn,
  UpdateDateColumn
} from "typeorm"
import { Building } from "./Building";


@Entity()
export class Power extends BaseEntity{
  /* primary Key */
  @PrimaryGeneratedColumn("increment") id: number;

  /* year (년도) */
  @Column({ "type": "int" })
  year: number;

  /* month (달) */
  @Column({ "type": "int" })
  month: number;

  /* day (일) */
  @Column({ "type": "int" })
  day: number;

  /* hour (시간) */
  @Column({ "type": "int" })
  hour: number;

  /* minute (분) */
  @Column({ "type": "int" })
  minute: number;

  /* value (전력 데이터) */
  @Column({ "type": "float" })
  value: number;

  /* Building Info (빌딩 데이터 정보) */
  @ManyToOne(type => Building, Building => Building.powers)
  building: Building[];

  @CreateDateColumn() createdAt: string;
  @UpdateDateColumn() updatedAt: string;
}

export default Power;