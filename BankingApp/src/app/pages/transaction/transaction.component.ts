import { Component, OnInit } from '@angular/core';
import { AccountService } from '../../service/acc.service'
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-transaction',
  standalone: true,
  imports: [ FormsModule, CommonModule ],
  templateUrl: './transaction.component.html',
  styleUrl: './transaction.component.css'
})
export class TransactionComponent {
  senderAccountNumber!: any;
  recipientAccountNumber!: any;
  amount!: any;

  constructor(private accountService: AccountService) { }

  makeTransactions(data: any) {
    this.senderAccountNumber = data.sender_account_number;
    this.recipientAccountNumber = data.recipient_account_number;
    this.amount = data.amount;
    this.accountService.makeTransaction(this.senderAccountNumber, this.recipientAccountNumber, this.amount).subscribe(
    (response: any) => {
      console.log(response);
    },
    (error) => {
      console.error(error);
    });
  }
}
