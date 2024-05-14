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

export class TransactionComponent implements OnInit {
  accounts: Account[] = [];
  transactionStatus!: string;

  constructor(private accountService: AccountService) { }

  ngOnInit(): void {
    this.loadAccounts();
  }

  makeTransactions(data: any) {
    const sender_account_number = data.sender_account_number;
    const recipient_account_number = data.recipient_account_number;
    const amount = data.amount;
    this.accountService.makeTransaction(sender_account_number, recipient_account_number, amount).subscribe(
    (response: any) => {
      console.log(response);
      this.transactionStatus = response.message;
    },
    (error) => {
      console.error(error);
      this.transactionStatus = error;
    });
  }

  loadAccounts() {
    this.accountService.getMyAccounts().subscribe(
      (response: string) => {
        const jsonResponse = JSON.parse(response); // Parse the JSON string
        this.accounts = jsonResponse as Account[]; // Map the parsed data into the accounts array
      },
      (error) => {
        console.error('Error fetching accounts:', error);
      }
    );
  }
}

export interface Account {
  AccountNumber: number
}