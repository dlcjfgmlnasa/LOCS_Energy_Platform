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
export class Broken extends BaseEntity{
  /* primary Key */
  @PrimaryGeneratedColumn("increment") id: number;

  /* value (고장 데이터) */
  @Column({ "type": "float" })
  value: number;

  /* Building Info (빌딩 데이터 정보) */
  @ManyToOne(type => Building, Building => Building.powers)
  building: Building[];

  @CreateDateColumn() createdAt: string;
  @UpdateDateColumn() updatedAt: string;
}

export default Broken;