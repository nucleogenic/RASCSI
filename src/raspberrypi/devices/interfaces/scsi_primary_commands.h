//---------------------------------------------------------------------------
//
// SCSI Target Emulator RaSCSI (*^..^*)
// for Raspberry Pi
//
// Copyright (C) 2021 Uwe Seimet
//
// Interface for SCSI primary commands (see https://www.t10.org/drafts.htm, SPC-6)
//
//---------------------------------------------------------------------------

#pragma once

class SASIDEV;

class ScsiPrimaryCommands
{
public:

	ScsiPrimaryCommands() {}
	virtual ~ScsiPrimaryCommands() {}

	// Mandatory commands
	virtual void TestUnitReady(SASIDEV *) = 0;
	virtual void Inquiry(SASIDEV *) = 0;
	virtual void ReportLuns(SASIDEV *) = 0;

	// Implemented for all RaSCSI device types
	virtual void RequestSense(SASIDEV *) = 0;
};
