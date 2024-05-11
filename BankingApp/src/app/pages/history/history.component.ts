import { Component } from '@angular/core';
import { AccountService } from '../../service/acc.service'
import { Time, CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-history',
  standalone: true,
  imports: [ FormsModule, CommonModule ],
  templateUrl: './history.component.html',
  styleUrl: './history.component.css'
})

export class HistoryComponent {
  logs: Log[] = [];
  accounts: Account[] = [];
  account_number!: number;

  ngOnInit(): void {
    this.loadAccounts();
  }

  constructor(private accountService: AccountService) { }

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

  loadLogs(account_number: number) {
    this.accountService.showLog(account_number).subscribe(
      (response: any) => {
        console.log(response);
        const jsonResponse = JSON.parse(response); // Parse the JSON string
        this.logs = jsonResponse as Log[]; // Map the parsed data into the logs array
        console.log(this.logs);
      },
      (error) => {
        console.error('Error fetching logs:', error);
      }
    )
  }
}

export interface Log {
  LogID: number,
  AccountNumber: number,
  Recipient: number,
  Amount: number,
  LogAction: string,
  LogTime: Time,
  LogDesc: string
}

export interface Account {
  AccountNumber: number
}