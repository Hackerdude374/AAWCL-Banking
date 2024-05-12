import { Component, OnInit } from '@angular/core';
import { AccountService } from '../../service/acc.service'
import { Time } from '@angular/common';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-cardmanagement',
  standalone: true,
  imports: [ CommonModule ],
  templateUrl: './cardmanagement.component.html',
  styleUrl: './cardmanagement.component.css'
})

export class CardmanagementComponent implements OnInit {

  cards: Card[] = [];
  cardStatus!: string;

  ngOnInit(): void {
    this.loadCards();
  }

  constructor(private accountService: AccountService) { }

  loadCards() {
    this.accountService.getMyCards().subscribe(
      (response: string) => {
        const jsonResponse = JSON.parse(response); // Parse the JSON string
        this.cards = jsonResponse as Card[]; // Map the parsed data into the accounts array
      },
      (error) => {
        console.error('Error fetching credit cards:', error);
        this.cardStatus = error;
      }
    );
  }

  changeCardStatus(card: Card) {
    const card_number = card.CardNumber;
    const card_status = card.newStatus;
    card.CardStatus = card_status;
    this.accountService.cardStatus(card_number, card_status).subscribe(
      (response: string) => {
        console.log(response);
      },
      (error) => {
        console.error('Error changing status:', error);
      }
    );
  }
}

export interface Card { 
  CardNumber: string,
  CardHolder: string,
  ExpirationDate: Time,
  Cvv: number,
  CardType: string,
  Balance: number
  CardStatus?: string,
  newStatus?: string
}